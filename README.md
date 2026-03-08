# Electra Smart AC — Community-Maintained Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Community-maintained fork of the official [Electra Smart](https://www.home-assistant.io/integrations/electrasmart) Home Assistant integration, originally developed by [@jafar-atili](https://github.com/jafar-atili).

The official integration and its underlying library ([pyElectra](https://github.com/jafar-atili/pyElectra)) appear to be abandoned — open issues have gone unanswered since mid-2024. This fork continues development and ships fixes for known bugs.

## Fixes Included

### Wrong Current Temperature (5,632°C instead of 22°C)

The `I_RAT` and `I_CALC_AT` telemetry values from the Electra API are raw integers left-shifted by 8 bits (×256). The official integration stores them without converting, causing absurd temperature readings.

| Raw value | Official integration | This fork |
|-----------|---------------------|-----------|
| 5,632 | 5,632°C | 22°C |
| 5,888 | 5,888°C | 23°C |
| 6,144 | 6,144°C | 24°C |

**Related upstream issues (unfixed):**
- [home-assistant/core#124409](https://github.com/home-assistant/core/issues/124409) — electrasmart showing wrong temp
- [home-assistant/core#160191](https://github.com/home-assistant/core/issues/160191) — electra smart not retrieving current temp properly
- [pyElectra PR#15](https://github.com/jafar-atili/pyElectra/pull/15) — upstream library fix (pending)

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3-dot menu → **Custom repositories**
3. Add `https://github.com/dormeljon/ha-electrasmart` as type **Integration**
4. Search for "Electra Smart" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/electrasmart` folder to your HA `config/custom_components/` directory
2. Restart Home Assistant

## How It Works

This custom component uses the same `electrasmart` domain as the official integration, so it automatically overrides it. No reconfiguration needed — your existing Electra Smart devices will use the fixed code immediately.

## Removal

If the official integration gets fixed upstream, simply uninstall this custom component via HACS and the built-in one will take over again.

## Contributing

Issues and PRs are welcome. This integration is based on the official HA core `electrasmart` component and the `pyElectra==1.2.4` library.

## Credits

- [@jafar-atili](https://github.com/jafar-atili) — original integration and pyElectra library
- [@dormeljon](https://github.com/dormeljon) — community maintenance and fixes
