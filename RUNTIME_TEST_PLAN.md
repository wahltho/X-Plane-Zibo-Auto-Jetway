# Runtime acceptance plan

Use a disposable stock Zibo 4.05.35 installation. Record the active config and
verify the native command separately from the automatic lifecycle.

## Persistence

| Case | Expected result |
|---|---|
| Config key absent | Tablet shows `ON` |
| `AUTO JETWAY = 1` | `ON` after aircraft reload and X-Plane restart |
| `AUTO JETWAY = 0` | `OFF` after aircraft reload and X-Plane restart |
| Invalid text, `-1` or `2` | Tablet shows `ON` |
| Livery config contains a conflicting value | Global value remains authoritative |
| Save another Tablet option | Global `AUTO JETWAY` value remains correct |

## Automatic lifecycle

Test each row at a stand where `B738DR_jetway_nearest <= 0.05`.

| Lifecycle | ON | OFF |
|---|---|---|
| Boarding/ground-service start | One native jetway toggle | No native jetway toggle |
| Boarding completion after L1/L2 close | One native jetway toggle | No native jetway toggle |
| Post-landing ground-service start | One native jetway toggle | No native jetway toggle |

For every row, compare state progression, boarding and cargo timers, door
targets, buses, stairs, belts and completion status. They must remain identical
apart from the native jetway action itself.

## Stand behavior

- Nearby stand with `OFF`: do not reclassify the stand or create remote stairs
  and buses as a fallback.
- Remote stand: preserve the original airstair and forward-stair behavior.
- Unknown or unavailable proximity: preserve the original behavior.

## Manual and external command

With the option set to both values, invoke `sim/ground_ops/jetway` through:

1. an X-Plane key or joystick assignment;
2. the X-Plane command UI or a command utility;
3. representative hardware or an external plugin, when available.

Every invocation must still reach X-Plane while `AUTO JETWAY` is `OFF`.

## Toggle timing

- Changing `ON -> OFF` must not issue a command or alter current doors/GSE.
- Changing `OFF -> ON` must not replay a lifecycle call already passed.
- No lifecycle point may issue duplicate calls on subsequent frames.
