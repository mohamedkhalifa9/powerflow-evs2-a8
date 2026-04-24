# Powerflow / EVS II Ü8

Small workspace for the exercise **“Engpassbehebung im Übertragungsnetz”** (3-bus 380 kV delta, two plants, two industrial loads, three lines with \(X' = 0{,}3\,\Omega/\mathrm{km}\)).

## Contents

| Item | Description |
|------|-------------|
| `EVS2_A8.py` | [pandapower](https://pandapower.readthedocs.io/) model: `ext_grid` (slack on bus 1), gens/loads, lines 50/100/150 km; `runpp` and bus angles in **rad** for comparison with the DC hand calculation. |
| `EVS_II_A8.pdf` | Assignment sheet. |
| `Powerflow_EVS2_A8.slx` | Simulink / powergui phasor model (optional cross-check; requires MATLAB and suitable toolbox). |
| `A8.png` | Diagram or screenshot reference. |
| `requirements.txt` | Python dependencies. |

`S_base` in the script is 100 MVA (conventional choice; the sheet does not fix a system base MVA).

## Python setup

```bash
cd /path/to/Powerflow
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python EVS2_A8.py
```

Use Python **3.10+**; tested with the versions pinned implicitly by the requirements (pandapower 3.x pulls `scipy` and other dependencies).

## Notes

- `runpp` is **AC**; the analytical Ü8.1/8.2 **Wirk-DC** angles will be **very close** but not bit-identical. For a DC check in pandapower, you can also run a DC power flow (`rundcpp`) and compare to the lecture formulas.
- The thermal line limit in the model uses **550 A** through `max_i_ka=0.55` on the lines; verify against your report convention.

## License

Private / coursework. Do not use course materials in violation of your university’s rules. Task provided by IAEW RWTH Aachen
