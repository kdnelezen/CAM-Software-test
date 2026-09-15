from __future__ import annotations

from pathlib import Path
from typing import Any

from .api import CAMSoftware
from .models import CAMJobConfig, MachineType, ToolConfig
from .version import __version__

APP_NAME = "CAM Software Test"


def machine_choices() -> list[str]:
    return [machine.value for machine in MachineType]


def default_output_path(input_path: str) -> str:
    source = Path(input_path)
    return str(source.with_suffix(".nc")) if source.suffix else f"{source}.nc"


def build_configs(
    machine: str,
    tool_number: int,
    tool_diameter: float,
    feed_rate: float,
    spindle_rpm: int,
    safe_z: float,
    cut_depth: float,
) -> tuple[CAMJobConfig, ToolConfig]:
    job = CAMJobConfig(
        machine_type=MachineType(machine),
        safe_z=safe_z,
        cut_depth=cut_depth,
    )
    tool = ToolConfig(
        tool_number=tool_number,
        diameter=tool_diameter,
        spindle_rpm=spindle_rpm,
        feed_rate=feed_rate,
    )
    return job, tool


def _load_tk() -> tuple[Any, Any, Any, Any]:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    return tk, filedialog, messagebox, ttk


class CAMDesktopApp:
    def __init__(self) -> None:
        tk, filedialog, messagebox, ttk = _load_tk()
        self._tk = tk
        self._filedialog = filedialog
        self._messagebox = messagebox
        self._ttk = ttk
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} {__version__}")
        self.root.resizable(False, False)
        self.cam = CAMSoftware()
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.machine = tk.StringVar(value=MachineType.MILL_3_AXIS.value)
        self.tool_number = tk.IntVar(value=1)
        self.tool_diameter = tk.DoubleVar(value=6.0)
        self.feed_rate = tk.DoubleVar(value=500.0)
        self.spindle_rpm = tk.IntVar(value=6000)
        self.safe_z = tk.DoubleVar(value=5.0)
        self.cut_depth = tk.DoubleVar(value=1.0)
        self._build_ui()

    def _build_ui(self) -> None:
        frame = self._ttk.Frame(self.root, padding=12)
        frame.grid(column=0, row=0, sticky="nsew")

        self._ttk.Label(frame, text="Input CAD file").grid(column=0, row=0, sticky="w")
        self._ttk.Entry(frame, textvariable=self.input_file, width=48).grid(column=0, row=1, sticky="ew")
        self._ttk.Button(frame, text="Browse…", command=self._select_input).grid(column=1, row=1, padx=(8, 0))

        self._ttk.Label(frame, text="Output G-code file").grid(column=0, row=2, sticky="w", pady=(10, 0))
        self._ttk.Entry(frame, textvariable=self.output_file, width=48).grid(column=0, row=3, sticky="ew")
        self._ttk.Button(frame, text="Browse…", command=self._select_output).grid(column=1, row=3, padx=(8, 0))

        self._ttk.Label(frame, text="Machine").grid(column=0, row=4, sticky="w", pady=(10, 0))
        self._ttk.Combobox(frame, textvariable=self.machine, values=machine_choices(), state="readonly", width=20).grid(
            column=0,
            row=5,
            sticky="w",
        )

        numeric_fields = [
            ("Tool number", self.tool_number),
            ("Tool diameter", self.tool_diameter),
            ("Feed rate", self.feed_rate),
            ("Spindle RPM", self.spindle_rpm),
            ("Safe Z", self.safe_z),
            ("Cut depth", self.cut_depth),
        ]
        for row_offset, (label, variable) in enumerate(numeric_fields, start=6):
            self._ttk.Label(frame, text=label).grid(
                column=0,
                row=row_offset,
                sticky="w",
                pady=(10 if row_offset == 6 else 4, 0),
            )
            self._ttk.Entry(frame, textvariable=variable, width=20).grid(column=0, row=row_offset + 1, sticky="w")

        self._ttk.Button(frame, text="Export G-code", command=self._export).grid(column=0, row=18, pady=(14, 0), sticky="w")

    def _select_input(self) -> None:
        selected = self._filedialog.askopenfilename(
            title="Select CAD file",
            filetypes=(("CAD files", "*.stl *.obj"), ("All files", "*.*")),
        )
        if selected:
            self.input_file.set(selected)
            if not self.output_file.get():
                self.output_file.set(default_output_path(selected))

    def _select_output(self) -> None:
        initial_name = Path(self.output_file.get()).name if self.output_file.get() else "output.nc"
        selected = self._filedialog.asksaveasfilename(
            title="Select G-code output",
            defaultextension=".nc",
            initialfile=initial_name,
            filetypes=(("G-code", "*.nc *.gcode"), ("All files", "*.*")),
        )
        if selected:
            self.output_file.set(selected)

    def _export(self) -> None:
        if not self.input_file.get() or not self.output_file.get():
            self._messagebox.showerror(APP_NAME, "Select both an input CAD file and an output G-code file.")
            return
        try:
            job, tool = build_configs(
                machine=self.machine.get(),
                tool_number=self.tool_number.get(),
                tool_diameter=self.tool_diameter.get(),
                feed_rate=self.feed_rate.get(),
                spindle_rpm=self.spindle_rpm.get(),
                safe_z=self.safe_z.get(),
                cut_depth=self.cut_depth.get(),
            )
            self.cam.export_gcode(
                file_path=self.input_file.get(),
                job=job,
                tool=tool,
                output_path=self.output_file.get(),
            )
        except Exception as exc:  # pragma: no cover - surfaced in UI only
            self._messagebox.showerror(APP_NAME, str(exc))
            return
        self._messagebox.showinfo(APP_NAME, f"Exported G-code to {self.output_file.get()}")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    try:
        CAMDesktopApp().run()
    except ModuleNotFoundError as exc:
        if exc.name == "tkinter":
            raise SystemExit("Desktop UI requires tkinter support. Use cam-cli in headless environments.") from exc
        raise
    except Exception as exc:
        if exc.__class__.__name__ == "TclError":
            raise SystemExit("Desktop UI requires a graphical session and tkinter support. Use cam-cli in headless environments.") from exc
        raise
