from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton,
                             QHBoxLayout, QMessageBox, QTextEdit, QLabel,
                             QSplitter, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QTextCharFormat, QFont
import os
import time
import datetime
import json


# ─────────────────────────────────────────────────────────────
# Background thread: executes the generated Python code safely
# ─────────────────────────────────────────────────────────────
class SequenceRunner(QThread):
    log_message      = pyqtSignal(str)          # text line to append to log
    run_finished     = pyqtSignal(bool, str)    # (success, final_message)
    images_captured  = pyqtSignal(list)         # list of {"name": ..., "path": ...}

    def __init__(self, code: str, test_params: dict, dut_data: dict = None):
        super().__init__()
        self.code       = code
        self.test_params = test_params
        self.dut_data   = dut_data or {}
        self._stop_flag  = False

    def stop(self):
        self._stop_flag = True

    def _detect_used_instruments(self):
        """Parse the generated code to find which instruments are actually referenced."""
        used = set()
        if "mgr.ac_source" in self.code:
            used.add("ac_source")
        if "mgr.dc_load" in self.code:
            used.add("dc_load")
        if "mgr.scope" in self.code:
            used.add("scope")
        return used

    def run(self):
        from instruments.manager import InstrumentManager
        mgr = InstrumentManager()
        
        def log_cb(msg):
            if self._stop_flag:
                raise InterruptedError("Sequence stopped by user")
            self.log_message.emit(msg)
            
        mgr.set_logger(log_cb)

        # Only connect instruments that appear in the generated code
        used = self._detect_used_instruments()
        if not used:
            log_cb("⚠ No instrument blocks detected — nothing to connect.")
        else:
            instrument_labels = {
                "ac_source": "Source (ac_source)",
                "dc_load":   "Load (dc_load)",
                "scope":     "Scope"
            }
            log_cb(f"⚡ Instruments needed: {', '.join(instrument_labels.get(i, i) for i in used)}")

            all_ok = True
            for inst_key in used:
                try:
                    driver = getattr(mgr, inst_key, None)
                    if driver is None:
                        log_cb(f"❌ No driver configured for '{inst_key}'")
                        all_ok = False
                        continue
                    if not driver.connected:
                        driver.connect()
                        log_cb(f"✅ Connected to {instrument_labels.get(inst_key, inst_key)}")
                except Exception as e:
                    log_cb(f"❌ Failed to connect {instrument_labels.get(inst_key, inst_key)}: {e}")
                    all_ok = False

            if not all_ok:
                log_cb("❌ Could not connect to all required instruments!")
                self.run_finished.emit(False, "Connection failed")
                return

        if not self.code or not self.code.strip():
            log_cb("⚠ Sequence is empty — nothing to run.")
            self.run_finished.emit(False, "Empty sequence")
            return

        log_cb("▶ Executing sequence…\n")

        images = []

        context = {
            "mgr":               mgr,
            "log_callback":      log_cb,
            "time":              time,
            "os":                os,
            "test_params":       self.test_params,
            "dut_data":          self.dut_data,
            "progress_callback": lambda v: None,   # no-op in editor
            "images":            images,
        }

        try:
            exec(self.code, context)   # noqa: S102
            if self._stop_flag:
                self.log_message.emit("\n⏹ Sequence stopped by user.")
                self.run_finished.emit(False, "Stopped")
            else:
                self.log_message.emit("\n✅ Sequence completed successfully.")
                if images:
                    self.images_captured.emit(images)
                self.run_finished.emit(True, "Done")
        except InterruptedError:
            self.log_message.emit("\n⏹ Sequence stopped by user.")
            self.run_finished.emit(False, "Stopped")
        except Exception as e:
            self.log_message.emit(f"\n❌ Runtime error: {e}")
            self.run_finished.emit(False, str(e))
        finally:
            # Safety: turn off outputs only for instruments that were used
            if "ac_source" in used:
                try:
                    mgr.ac_source.output_off()
                    self.log_message.emit("🔒 Source output turned OFF (safety).")
                except Exception:
                    pass
            if "dc_load" in used:
                try:
                    mgr.dc_load.load_off()
                    self.log_message.emit("🔒 Load turned OFF (safety).")
                except Exception:
                    pass


# ─────────────────────────────────────────────────────────────
# Block Editor Window
# ─────────────────────────────────────────────────────────────
class BlockEditorWindow(QMainWindow):
    def __init__(self, test_name, test_params=None, existing_xml=None,
                 on_save_callback=None, dut_data=None):
        super().__init__()
        self.setWindowTitle(f"Block Editor — {test_name}")
        self.resize(1200, 850)

        self.test_name   = test_name
        self.test_params = test_params or {}
        self.dut_data    = dut_data or {}
        self.on_save     = on_save_callback
        self._runner: SequenceRunner | None = None

        print(f"BlockEditor initialized with XML: {str(existing_xml)[:50]}…")

        # ── Central widget ──
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Vertical splitter: Blockly editor (top) / Log panel (bottom) ──
        splitter = QSplitter(Qt.Orientation.Vertical)
        root_layout.addWidget(splitter)

        # ── Top: Blockly web view ──
        self.webview = QWebEngineView()
        splitter.addWidget(self.webview)

        # ── Bottom: Run log panel ──
        log_frame = QFrame()
        log_frame.setStyleSheet("background:#1a1a2e;")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(6, 4, 6, 4)
        log_layout.setSpacing(3)

        log_header = QLabel("  📋 Sequence Run Log")
        log_header.setStyleSheet(
            "color:#a0aec0; font-size:11px; font-weight:bold; padding:2px 0;"
        )
        log_layout.addWidget(log_header)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFont(QFont("Consolas", 9))
        self.log_area.setStyleSheet(
            "background:#0f0f23; color:#c3e88d; border:1px solid #2d3748;"
            "border-radius:4px; padding:4px;"
        )
        self.log_area.setPlaceholderText(
            "Press ▶ Run Sequence to execute blocks and see live output here…"
        )
        self.log_area.setFixedHeight(180)
        log_layout.addWidget(self.log_area)
        splitter.addWidget(log_frame)

        splitter.setSizes([620, 180])

        # ── Button bar ──
        btn_bar = QWidget()
        btn_bar.setStyleSheet("background:#16213e; border-top:1px solid #2d3748;")
        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(10, 6, 10, 6)
        btn_layout.setSpacing(8)

        # Left side: run controls
        self.run_btn = QPushButton("▶  Run Sequence")
        self.run_btn.setObjectName("RunButton")
        self.run_btn.setToolTip("Execute the current blocks directly (connects to instruments)")
        self.run_btn.clicked.connect(self.run_sequence)
        self._style_btn(self.run_btn, "#22c55e", "#16a34a")

        self.stop_btn = QPushButton("⏹  Stop")
        self.stop_btn.setToolTip("Stop the currently running sequence")
        self.stop_btn.clicked.connect(self.stop_sequence)
        self.stop_btn.setEnabled(False)
        self._style_btn(self.stop_btn, "#ef4444", "#dc2626")

        self.clear_log_btn = QPushButton("🗑  Clear Log")
        self.clear_log_btn.setToolTip("Clear the run log panel")
        self.clear_log_btn.clicked.connect(self.log_area.clear)
        self._style_btn(self.clear_log_btn, "#4b5563", "#374151")

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_log_btn)
        btn_layout.addStretch()

        # Right side: save / cancel
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setToolTip("Close without saving")
        cancel_btn.clicked.connect(self._safe_close)
        self._style_btn(cancel_btn, "#4b5563", "#374151")

        save_btn = QPushButton("💾  Save Sequence")
        save_btn.setToolTip("Save sequence and close editor")
        save_btn.clicked.connect(self.save_sequence)
        self._style_btn(save_btn, "#3b82f6", "#2563eb")

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        root_layout.addWidget(btn_bar)

        # ── Load Blockly editor ──
        if existing_xml:
            self.pending_xml = existing_xml
            self.webview.loadFinished.connect(
                lambda: QTimer.singleShot(500, self.inject_xml_and_params)
            )
        else:
            self.pending_xml = None
            self.webview.loadFinished.connect(
                lambda: QTimer.singleShot(500, self.inject_params_only)
            )

        editor_path = os.path.abspath("assets/blockly/editor.html")
        self.webview.setUrl(QUrl.fromLocalFile(editor_path))
        self.webview.page().javaScriptConsoleMessage = self._js_console

    # ── Helpers ────────────────────────────────────────────────

    @staticmethod
    def _style_btn(btn: QPushButton, bg: str, hover: str):
        btn.setStyleSheet(
            f"QPushButton {{"
            f"  background:{bg}; color:#fff; border:none;"
            f"  border-radius:5px; padding:6px 14px; font-weight:600;"
            f"}}"
            f"QPushButton:hover {{ background:{hover}; }}"
            f"QPushButton:disabled {{ background:#374151; color:#6b7280; }}"
        )

    def _js_console(self, level, message, line, source):
        print(f"JS [{level}]: {message}  (line {line})")

    def _append_log(self, text: str):
        """Append a timestamped line to the log panel (thread-safe via signal)."""
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{ts}]  {text}")
        # Auto-scroll to bottom
        sb = self.log_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _safe_close(self):
        if self._runner and self._runner.isRunning():
            reply = QMessageBox.question(
                self, "Sequence Running",
                "A sequence is currently running.\nStop it and close the editor?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_sequence()
                QTimer.singleShot(600, self.close)
        else:
            self.close()

    # ── Blockly injection ──────────────────────────────────────

    def inject_params_only(self):
        param_keys = list(self.test_params.keys())
        print(f"Injecting Params: {param_keys}")
        js_params = json.dumps(param_keys)
        self.webview.page().runJavaScript(f"setAvailableParams({js_params});")

    def inject_xml_and_params(self):
        self.inject_params_only()
        if self.pending_xml:
            print(f"Injecting XML: {self.pending_xml[:50]}…")
            json_xml = json.dumps(self.pending_xml)
            self.webview.page().runJavaScript(f"setXML(JSON.parse({json_xml}));")
            self.pending_xml = None
        else:
            print("No pending XML to inject.")

    # ── Save ──────────────────────────────────────────────────

    def save_sequence(self):
        self.webview.page().runJavaScript("getPythonCode()", self._handle_code_for_save)

    def _handle_code_for_save(self, python_code):
        self.generated_code = python_code
        self.webview.page().runJavaScript("getXML()", self._handle_xml_for_save)

    def _handle_xml_for_save(self, xml_text):
        self.xml_content = xml_text
        if self.on_save:
            self.on_save(self.test_name, self.generated_code, self.xml_content)
        QMessageBox.information(self, "Saved", "Sequence saved successfully.")
        self.close()

    # ── Run Sequence ───────────────────────────────────────────

    def run_sequence(self):
        """Fetch current Python code from Blockly and execute it."""
        if self._runner and self._runner.isRunning():
            QMessageBox.warning(self, "Already Running",
                                "A sequence is already running. Stop it first.")
            return
        # Step 1: get the generated Python code from JS
        self.webview.page().runJavaScript("getPythonCode()", self._handle_code_for_run)

    def _handle_code_for_run(self, python_code: str):
        if not python_code or not python_code.strip():
            QMessageBox.warning(self, "Empty Sequence",
                                "The workspace is empty — add some blocks first.")
            return

        # Show the code in log for transparency
        self.log_area.clear()
        self._append_log("═" * 55)
        self._append_log(f"  TEST: {self.test_name}")
        self._append_log("═" * 55)
        self._append_log("Generated Python code:")
        for line in python_code.splitlines():
            self._append_log(f"   {line}")
        self._append_log("─" * 55)
        self._append_log("")

        # Update button states
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.run_btn.setText("⏳  Running…")

        # Launch runner thread
        self._runner = SequenceRunner(
            code=python_code,
            test_params=self.test_params,
            dut_data=self.dut_data
        )
        self._runner.log_message.connect(self._append_log)
        self._runner.images_captured.connect(self._on_images_captured)
        self._runner.run_finished.connect(self._on_run_finished)
        self._runner.start()

    def _on_images_captured(self, images: list):
        """Called when the runner emits captured image paths."""
        self._last_captured_images = images
        if images:
            self._append_log("")
            self._append_log(f"📸  {len(images)} image(s) captured:")
            for img in images:
                self._append_log(f"   → {img.get('name', 'Image')}: {img.get('path', '?')}")

    def _on_run_finished(self, success: bool, message: str):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("▶  Run Sequence")
        self.stop_btn.setEnabled(False)

        captured = getattr(self, '_last_captured_images', [])
        self._last_captured_images = []  # reset for next run

        if success:
            self._append_log("─" * 55)
            self._append_log("✅  Run complete.")
            # Non-blocking notification
            msg = QMessageBox(self)
            msg.setWindowTitle("Run Complete")
            detail = f"Sequence '{self.test_name}' finished successfully."
            if captured:
                detail += f"\n\n📸 {len(captured)} image(s) saved to:\n"
                for img in captured:
                    detail += f"  • {img.get('path', '?')}\n"
            msg.setText(detail)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.show()
        else:
            self._append_log("─" * 55)
            self._append_log(f"⚠  Run ended: {message}")

    # ── Stop Sequence ──────────────────────────────────────────

    def stop_sequence(self):
        if self._runner and self._runner.isRunning():
            self._runner.stop()
            self._append_log("⏹  Stop requested — waiting for thread to finish…")
            # The stop flag is only checked from the log callback, so a sequence
            # blocked inside a long Wait block (time.sleep) won't react until it
            # wakes up on its own. Force it after a grace period so Stop doesn't
            # silently do nothing — mirrors the emergency-stop behavior used
            # elsewhere in the app.
            QTimer.singleShot(2000, self._force_stop_if_still_running)

    def _force_stop_if_still_running(self):
        if self._runner and self._runner.isRunning():
            self._append_log("⏹  Sequence did not stop in time — forcing termination.")
            self._runner.terminate()
            self._runner.wait(2000)
            self._safety_shutdown()
            self._on_run_finished(False, "Force-stopped")

    def _safety_shutdown(self):
        """Best-effort: turn off source/load outputs after a forced stop."""
        try:
            from instruments.manager import InstrumentManager
            mgr = InstrumentManager()
            try:
                if mgr.ac_source and mgr.ac_source.connected:
                    mgr.ac_source.output_off()
                    self._append_log("🔒 Source output turned OFF (safety).")
            except Exception:
                pass
            try:
                if mgr.dc_load and mgr.dc_load.connected:
                    mgr.dc_load.load_off()
                    self._append_log("🔒 Load turned OFF (safety).")
            except Exception:
                pass
        except Exception as e:
            self._append_log(f"⚠ Safety shutdown error: {e}")
