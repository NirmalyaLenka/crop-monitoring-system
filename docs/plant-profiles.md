# Plant Profiles: Values, Sources, and Precautions

This document explains the reasoning behind each plant script's threshold values, and lists precautions specific to each plant. All ranges are general guidance for hobby greenhouse growing, gathered from widely published horticultural growing guidance, and simplified into single monitoring bands for this beginner project. They are a helpful baseline, not a substitute for observing your specific plant variety, local climate, and growing method.

## Important Simplifications to Understand

- **Temperature is a single day/night band.** Real growing guidance often separates day and night targets. This project combines them into one range per plant to keep monitoring simple. If you want tighter control, you can edit the `temperature_c` tuple in any plant script and consider adding separate day/night logic as a future upgrade.
- **Soil/substrate moisture is a percentage estimated from a two-point calibration**, not a scientific soil-moisture-content measurement. Calibrate your own sensor as described in `docs/hardware-setup.md`, and treat the percentage as a relative trend indicator, not an absolute number to compare against generic gardening advice written for a different measurement method.
- **Air quality (MQ135) is not a calibrated CO2 or ppm sensor.** It is a low-cost hobby sensor that responds to a mix of gases. Treat its threshold as "notably worse than my own fresh air baseline," calibrated per `docs/hardware-setup.md`, not as an absolute safety limit.
- **Light is measured in lux**, a measure of light intensity, not total daily light exposure (growers sometimes use Daily Light Integral, or DLI, which also accounts for duration). This project only checks instantaneous lux level as a simple proxy for "is it currently bright enough," which is a simplification.

## Mushroom (Oyster Mushroom, Fruiting Stage)

| Parameter | Range used | Why |
|---|---|---|
| Temperature | 15 to 21 C | Oyster mushrooms fruit best in cool, stable conditions; higher temperatures can cause faster, weaker growth and higher contamination risk |
| Humidity | 85 to 95% | Mushrooms lose moisture quickly through their caps and need very high ambient humidity to develop properly |
| Substrate moisture | 70 to 95% (calibrated estimate) | The growing substrate needs to stay consistently damp, not waterlogged |
| Light | 200 to 1000 lux | Low, indirect, diffused light is enough; mushrooms do not photosynthesize like plants, but some light exposure helps trigger and orient fruiting |
| Air quality | Calibrate to fresh-air baseline | CO2 buildup is a major issue for mushrooms specifically; poor fresh air exchange causes long, thin stems and small, underdeveloped caps |

**Precautions specific to mushrooms:**

- Fresh air exchange is critical. A sealed, humid grow tent with no ventilation will build up CO2 quickly and ruin a fruiting flush, even if temperature and humidity look perfect.
- High humidity for extended periods is hard on electronics. Keep the Pi, camera, and any non-waterproof components outside the humid chamber, or in a sealed enclosure with only the sensor probes and camera lens exposed.
- Contamination is a real risk in mushroom cultivation. Basic cleanliness (clean hands, sanitized tools, and a well-ventilated grow space) matters more for successful mushroom growing than any single sensor reading.
- Avoid direct water spray onto electronics when misting the growing chamber.

## Tomato

| Parameter | Range used | Why |
|---|---|---|
| Temperature | 15 to 27 C | Combines a day range of roughly 22-27 C with a cooler night range of roughly 15-21 C |
| Humidity | 60 to 70% | Balances enough moisture for healthy growth against the fungal disease risk of overly humid, stagnant air |
| Soil moisture | 60 to 80% (calibrated estimate) | Tomatoes prefer evenly moist soil and dislike both drought stress and waterlogging |
| Light | 10,000 to 130,000 lux | Tomatoes need strong light, ideally 6 to 8 or more hours of direct sun equivalent per day |
| Air quality | Calibrate to fresh-air baseline | General air freshness check; good ventilation also reduces fungal disease pressure |

**Precautions specific to tomatoes:**

- Water at the base of the plant, not over the leaves. Wet foliage combined with high humidity is a common cause of fungal diseases like blight.
- Support tall or heavily fruiting plants with stakes or cages to prevent stem damage.
- Watch for consistent overwatering symptoms (yellowing leaves, splitting fruit) even if the sensor reading looks acceptable, since a single moisture probe cannot capture the whole root zone.

## Citrus

| Parameter | Range used | Why |
|---|---|---|
| Temperature | 10 to 29 C | Growth stalls below about 10 C, and frost risk becomes serious well below that; upper end reflects typical warm greenhouse daytime conditions |
| Humidity | 50 to 60% | Moderate humidity suits most citrus varieties without encouraging fungal issues |
| Soil moisture | 35 to 65% (calibrated estimate) | Citrus generally prefers the topsoil to dry out somewhat between waterings rather than staying constantly wet |
| Light | 8,000 to 130,000 lux | Citrus needs strong light, ideally 6 to 8 hours or more of direct sun equivalent per day |
| Air quality | Calibrate to fresh-air baseline | General air freshness check |

**Precautions specific to citrus:**

- Cold damage and frost are the biggest risk. If your setup is in a region with cold nights, plan for supplemental heating or moving potted citrus indoors well before temperatures approach freezing.
- Avoid letting citrus sit in waterlogged soil, which is a common cause of root rot in potted citrus trees.
- Citrus trees can take a long time to show visible stress, so do not rely only on how the plant looks; trust the logged sensor history as well.

## Pepper (Bell Pepper or Chili Pepper)

| Parameter | Range used | Why |
|---|---|---|
| Temperature | 15 to 27 C | Combines a day range of roughly 21-27 C with a cooler night range of roughly 15-21 C |
| Humidity | 50 to 70% | Peppers tolerate a fairly wide humidity band but do best avoiding extremes |
| Soil moisture | 55 to 75% (calibrated estimate) | Peppers want consistently moist soil without waterlogging |
| Light | 10,000 to 130,000 lux | Peppers need at least 6 hours of strong direct light daily to fruit well |
| Air quality | Calibrate to fresh-air baseline | General air freshness check |

**Precautions specific to peppers:**

- Avoid wetting the foliage when watering, especially in humid conditions, to reduce fungal disease risk.
- Sudden temperature swings can cause flower or fruit drop, so try to keep conditions as stable as the ranges above rather than letting them swing between the extremes.
- Peppers are sensitive to overwatering in the seedling stage in particular; be more conservative with moisture for young plants.

## Mandevilla

| Parameter | Range used | Why |
|---|---|---|
| Temperature | 15 to 32 C | Cold sensitivity becomes a real risk below about 10 C, so 15 C is used as a safer lower alert threshold with margin |
| Humidity | 50 to 60% | Moderate humidity suits this tropical vine without encouraging fungal issues on its leaves |
| Soil moisture | 45 to 70% (calibrated estimate) | Mandevilla prefers to dry out slightly at the surface between waterings rather than sitting constantly wet |
| Light | 8,000 to 130,000 lux | Mandevilla flowers best with strong light, ideally 6 or more hours of direct sun equivalent daily, though it tolerates some partial shade |
| Air quality | Calibrate to fresh-air baseline | General air freshness check |

**Precautions specific to Mandevilla:**

- This is a tropical vine and is genuinely cold-sensitive; protect it well before temperatures approach 10 C.
- Mandevilla sap can be irritating to skin and is toxic if ingested, so wear gloves when pruning or handling cut stems, and keep cuttings away from children and pets.
- Overwatering is a more common problem than underwatering for potted Mandevilla; err toward the drier end of the moisture range if unsure.

## A Note on Accuracy

These values are a reasonable, research-informed starting point for a hobby setup, drawn from widely available general growing guidance rather than a single authoritative source. Local climate, specific plant varieties, growing medium, and pot or bed size all affect what "ideal" actually looks like for your setup. Use the alerts from this system as a prompt to check on your plants, not as an automatic diagnosis, and adjust the ranges in each plant script over time based on what you observe actually works for your own greenhouse.
