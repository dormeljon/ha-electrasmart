# Electra Smart AC - Fixed Integration for Home Assistant

Drop-in replacement for the official [Electra Smart](https://www.home-assistant.io/integrations/electrasmart) integration that fixes the **wrong current temperature** bug.

## The Problem

The official integration displays wildly incorrect temperatures:

| Raw value | Displayed | Actual |
|-----------|-----------|--------|
| 5,632 | 5,632°C | 22°C |
| 5,888 | 5,888°C | 23°C |
| 6,144 | 6,144°C | 24°C |

The root cause is in the [pyElectra](https://github.com/jafar-atili/pyElectra) library: the `I_RAT` and `I_CALC_AT` telemetry values are raw integers left-shifted by 8 bits (×256), but the library stores them without converting.

**Related issues:**
- [home-assistant/core#124409](https://github.com/home-assistant/core/issues/124409)
- [home-assistant/core#160191](https://github.com/home-assistant/core/issues/160191)
- [pyElectra PR#15](https://github.com/jafar-atili/pyElectra/pull/15) (upstream fix, pending)

## The Fix

This custom component applies the fix at the integration level by right-shifting (`>> 8`) the raw temperature value before exposing it to Home Assistant.

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3-dot menu → **Custom repositories**
3. Add `https://github.com/dormeljon/ha-electrasmart-fix` as type **Integration**
4. Search for "Electra Smart (Fixed)" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/electrasmart` folder to your HA `config/custom_components/` directory
2. Restart Home Assistant

The custom component overrides the official integration automatically (same `domain`). No reconfiguration needed — your existing Electra Smart setup will use the fixed code.

## Removal

If the official integration gets fixed upstream, simply uninstall this custom component and the official one will take over again.
