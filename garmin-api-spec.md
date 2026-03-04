# Garmin Connect API Documentation

This document covers nine Garmin Connect APIs (curl commands copied from browser developer tools).

---

## API 1: Activity List Search

Curl command examples (copied from browser developer tools):

**Example 1: Text search**

```bash
curl 'https://connect.garmin.com/gc-api/activitylist-service/activities/search/activities?search=black&limit=20&start=0' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i' --output temp
```

**Example 2: Filter by activity type and date range**

```bash
curl 'https://connect.garmin.com/gc-api/activitylist-service/activities/search/activities?activityType=running&startDate=2026-01-01&endDate=2026-02-13&limit=20&excludeChildren=false&start=0' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Query Parameters

| Parameter | Type | Required | Example | Notes |
|-----------|------|----------|---------|-------|
| `limit` | number | Yes | `20` | Max number of activities to return |
| `start` | number | Yes | `0` | Offset for pagination (0-indexed) |
| `search` | string | No | `"black"` | Free-text search across activity names |
| `activityType` | string | No | `"running"`, `"racket_sports"` | Filter by **parent** activity type key. Known parents: `"running"`, `"cycling"`, `"racket_sports"`, `"winter_sports"`, `"fitness_equipment"`. |
| `activitySubType` | string | No | `"trail_running"`, `"tennis_v2"` | Filter by activity sub-type key. Must be used together with `activityType`. See parent→sub-type mapping below. |
| `startDate` | string | No | `"2026-01-01"` | Filter start date (YYYY-MM-DD), inclusive |
| `endDate` | string | No | `"2026-02-13"` | Filter end date (YYYY-MM-DD), inclusive |
| `excludeChildren` | boolean | No | `false` | Whether to exclude child activities (multi-sport sub-activities) |

## File Format

- **File**: `temp` (no extension)
- **Compression**: Brotli (`.br`)
- **Underlying format**: JSON array
- **Compressed size**: 14,460 bytes
- **Decompressed size**: 112,264 bytes

## How to Decompress / Read

### Node.js (recommended — no extra dependencies)

```js
const fs = require('fs');
const zlib = require('zlib');

const compressed = fs.readFileSync('temp');
const json = JSON.parse(zlib.brotliDecompressSync(compressed).toString());
// json is an Array of activity objects
```

### Save as plain JSON

```js
const fs = require('fs');
const zlib = require('zlib');
fs.writeFileSync(
  'activities.json',
  zlib.brotliDecompressSync(fs.readFileSync('temp'))
);
```

### CLI (requires brotli installed)

```bash
mv temp temp.json.br
brotli -d temp.json.br -o activities.json
```

### Python

```python
import json, zlib
# Requires: pip install brotli
import brotli

with open('temp', 'rb') as f:
    data = json.loads(brotli.decompress(f.read()))
```

---

## Data Overview

- **Total activities**: 20
- **Date range**: 2025-01-02 to 2026-02-21
- **Activity types**: `trail_running` (10 activities), `pilates` (10 activities)
- **Source**: Garmin Connect (device manufacturer: GARMIN)

### Activity List

| # | Type | Name | Date (Local) | Distance | Duration |
|---|------|------|--------------|----------|----------|
| 0 | trail_running | Rancho San Antonio -> Black Mountain -> Skyline Ridge | 2026-02-21 07:17 | 35.7 km | 315 min |
| 1 | trail_running | Black Mountain | 2026-01-31 07:26 | 28.6 km | 227 min |
| 2 | trail_running | Black Mountain | 2026-01-24 07:13 | 26.2 km | 200 min |
| 3 | trail_running | Black Mountain | 2026-01-19 08:00 | 22.8 km | 176 min |
| 4 | trail_running | Black Mountain | 2026-01-10 07:14 | 26.0 km | 186 min |
| 5 | trail_running | Black Mountain | 2025-12-07 08:08 | 21.0 km | 175 min |
| 6 | trail_running | Black Mountain | 2025-11-29 08:29 | 21.0 km | 164 min |
| 7 | trail_running | Black Mountain and Rancho San Antonio | 2025-09-06 07:37 | 38.7 km | 326 min |
| 8 | pilates | Strengthen Your Back | 2025-08-25 20:56 | 0 km | 13 min |
| 9 | trail_running | Rancho San Antonio -> Black Mountain | 2025-08-09 08:07 | 30.5 km | 269 min |
| 10 | trail_running | Rancho San Antonio -> Black Mountain Summit | 2025-08-02 08:24 | 24.3 km | 188 min |
| 11 | pilates | Strengthen Your Back | 2025-04-29 20:56 | 0 km | 7 min |
| 12 | pilates | Strengthen Your Back | 2025-04-22 07:47 | 0 km | 13 min |
| 13 | pilates | Strengthen Your Back | 2025-04-16 07:54 | 0 km | 13 min |
| 14 | pilates | Strengthen Your Back | 2025-02-11 20:57 | 0 km | 13 min |
| 15 | pilates | Strengthen Your Back | 2025-02-03 20:44 | 0 km | 13 min |
| 16 | pilates | Strengthen Your Back | 2025-01-20 21:08 | 0 km | 13 min |
| 17 | pilates | Strengthen Your Back | 2025-01-09 20:53 | 0 km | 13 min |
| 18 | pilates | Strengthen Your Back | 2025-01-04 17:43 | 0 km | 13 min |
| 19 | pilates | Strengthen Your Back | 2025-01-02 08:07 | 0 km | 13 min |

---

## Field Reference — Complete List

Every activity object contains all fields listed below. Fields marked with **(trail only)** are `null` for pilates activities. Fields marked with **(sparse)** are `null` for some activities even within their type.

### Identity & Metadata

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `activityId` | number | `21942154782` | Unique Garmin activity ID |
| `activityUUID` | string | `"2e35002b-3559-437c-a985-d924ac276e73"` | UUID format |
| `activityName` | string | `"Black Mountain - Trail Running"` | User-editable name |
| `description` | string \| null | `"with Deliang"` | **(sparse)** — null in 11/20 |
| `activityType` | object | See below | Structured type info |
| `eventType` | object | `{"typeId":9,"typeKey":"uncategorized","sortOrder":10}` | |
| `sportTypeId` | number | `1` (running), `4` (pilates) | |
| `favorite` | boolean | `false` | User-starred |
| `pr` | boolean | `false` | Personal record flag |
| `parent` | boolean | `false` | |
| `manualActivity` | boolean | `false` | |
| `autoCalcCalories` | boolean | `false` | |
| `purposeful` | boolean | `false` | |
| `elevationCorrected` | boolean | `false` | |
| `atpActivity` | boolean | `false` | |
| `qualifyingDive` | boolean | `false` | |
| `decoDive` | boolean | `false` | |

#### `activityType` Object

```json
{
  "typeId": 6,
  "typeKey": "trail_running",
  "parentTypeId": 1,
  "isHidden": false,
  "restricted": false,
  "trimmable": true
}
```

**Parent vs Sub-type distinction**: Activity types have a hierarchy. The API supports filtering by both `activityType` (parent) and `activitySubType` (sub-type). Sub-type keys are often non-obvious (e.g., `"tennis_v2"` not `"tennis"`, `"resort_skiing_snowboarding_ws"` not `"skiing"`). Inspect `activityType.typeKey` in search results to discover actual keys.

Known parent→sub-type mappings:

| Parent (`activityType`) | Sub-types (`activitySubType`) |
|---|---|
| `running` | `running` (road/generic), `trail_running`, `treadmill_running`, `track_running` |
| `cycling` | *(sub-types TBD)* |
| `racket_sports` | `tennis_v2`, `pickleball` |
| `winter_sports` | `resort_skiing_snowboarding_ws` |
| `fitness_equipment` | `pilates`, `strength_training` |

**Naming overlap**: Some parent type keys are reused as sub-type `typeKey` values in the response. For example, `running` is both the parent type and the `typeKey` for road/generic runs. When the user says "running", they typically mean **all running** (the parent category), not just the `running` sub-type. Be careful not to treat the `running` typeKey as a distinct sub-category — present it as "road/generic running" when breaking down sub-types, and use "all running" when referring to the parent.

### Time

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `startTimeLocal` | string | `"2026-02-21 07:17:22"` | Local timezone |
| `startTimeGMT` | string | `"2026-02-21 15:17:22"` | UTC |
| `endTimeGMT` | string | `"2026-02-21 20:32:20"` | UTC |
| `beginTimestamp` | number | `1771687042000` | Unix ms |
| `timeZoneId` | number | `121` | Garmin timezone ID |
| `duration` | number | `18898.877` | Total duration in **seconds** |
| `elapsedDuration` | number | `18898.877` | Elapsed time in **seconds** |
| `movingDuration` | number | `18276.639` | Moving time in **seconds** |

### Distance, Speed & Cadence

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `distance` | number | `35716.82` | Total distance in **meters** |
| `averageSpeed` | number | `1.89` | In **m/s** |
| `maxSpeed` | number \| null | `3.938` | In **m/s** — **(trail only)** |
| `avgGradeAdjustedSpeed` | number \| null | `2.229` | In **m/s** — **(trail only)** |
| `steps` | number | `43102` | Total step count |
| `lapCount` | number | `36` | |
| `averageRunningCadenceInStepsPerMinute` | number | `121.64` | Steps/min |
| `maxRunningCadenceInStepsPerMinute` | number | `246` | |
| `maxDoubleCadence` | number | `246` | |

### Elevation

All elevation fields are **(trail only)** — `null` for pilates.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `elevationGain` | number \| null | `1585.54` | In **meters** |
| `elevationLoss` | number \| null | `1580.83` | In **meters** |
| `minElevation` | number \| null | `107.6` | In **meters** |
| `maxElevation` | number \| null | `860.8` | In **meters** |
| `avgElevation` | number \| null | `545.37` | In **meters** — null in 19/20 (very sparse) |
| `maxVerticalSpeed` | number \| null | `1.8` | In **m/s** |

### Heart Rate

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `averageHR` | number | `129` | BPM |
| `maxHR` | number | `154` | BPM |
| `hrTimeInZone_1` | number | `10778.218` | Time in **seconds** in HR zone 1 |
| `hrTimeInZone_2` | number | `7691.579` | Time in **seconds** in HR zone 2 |
| `hrTimeInZone_3` | number | `288.749` | Time in **seconds** in HR zone 3 |
| `hrTimeInZone_4` | number | `0` | Time in **seconds** in HR zone 4 |
| `hrTimeInZone_5` | number | `0` | Time in **seconds** in HR zone 5 |

### Power (Running Power)

All power fields are **(trail only)** — `null` for pilates.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `avgPower` | number \| null | `192` | In **watts** |
| `maxPower` | number \| null | `437` | In **watts** |
| `normPower` | number \| null | `222` | Normalized power in **watts** |
| `powerTimeInZone_1` | number \| null | `3744.433` | In **seconds** |
| `powerTimeInZone_2` | number \| null | `956.922` | In **seconds** |
| `powerTimeInZone_3` | number \| null | `217.972` | In **seconds** |
| `powerTimeInZone_4` | number \| null | `69.959` | In **seconds** |
| `powerTimeInZone_5` | number \| null | `0` | In **seconds** |

### Running Dynamics

All fields are **(trail only)** — `null` for pilates.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `avgVerticalOscillation` | number \| null | `7.04` | In **cm** |
| `avgGroundContactTime` | number \| null | `309.9` | In **milliseconds** |
| `avgStrideLength` | number \| null | `85.3` | In **cm** |
| `avgVerticalRatio` | number \| null | `8.45` | Percentage |

### Calories & Fitness

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `calories` | number | `2798` | Total kcal |
| `bmrCalories` | number | `447` | Basal metabolic kcal |
| `vO2MaxValue` | number \| null | `55` | **(sparse)** — null in 11/20 |
| `waterEstimated` | number | `2941` | Estimated water loss in **mL** |

### Training Effect & Load

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `aerobicTrainingEffect` | number | `4.1` | Scale 0–5 |
| `anaerobicTrainingEffect` | number | `0` | Scale 0–5 |
| `activityTrainingLoad` | number | `183.28` | EPOC-based training load |
| `trainingEffectLabel` | string | `"AEROBIC_BASE"` | |
| `aerobicTrainingEffectMessage` | string | `"HIGHLY_IMPROVING_AEROBIC_ENDURANCE_10"` | |
| `anaerobicTrainingEffectMessage` | string | `"NO_ANAEROBIC_BENEFIT_0"` | |
| `moderateIntensityMinutes` | number | `119` | In **minutes** |
| `vigorousIntensityMinutes` | number | `181` | In **minutes** |
| `differenceBodyBattery` | number | `-28` | Body battery change |

### Location & GPS

All location fields are **(trail only)** — `null` for pilates.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `startLatitude` | number \| null | `37.333` | Decimal degrees |
| `startLongitude` | number \| null | `-122.088` | Decimal degrees |
| `endLatitude` | number \| null | `37.333` | Decimal degrees |
| `endLongitude` | number \| null | `-122.088` | Decimal degrees |
| `locationName` | string \| null | `"Santa Clara County"` | Reverse-geocoded |
| `hasPolyline` | boolean | `true` | Whether GPS track exists |
| `hasHeatMap` | boolean | `false` | |

### Fastest Splits (Pace Records)

All are **(trail only)** — `null` for pilates. Values are in **seconds**.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `fastestSplit_1000` | number \| null | `311.57` | Fastest 1 km split |
| `fastestSplit_1609` | number \| null | `515.06` | Fastest 1 mile split |
| `fastestSplit_5000` | number \| null | `1838.51` | Fastest 5 km split |
| `fastestSplit_10000` | number \| null | `4053.06` | Fastest 10 km split |
| `fastestSplit_21098` | number \| null | `10930.91` | Fastest half marathon — **(sparse)** null in 12/20 (only for long runs) |

### Split Summaries

`splitSummaries` is an **array of objects**, each summarizing a category of splits within the activity.

#### Split Types Found

| `splitType` | Meaning |
|-------------|---------|
| `RWD_RUN` | Running segments |
| `RWD_WALK` | Walking segments |
| `RWD_STAND` | Standing/stopped segments |
| `INTERVAL_ACTIVE` | Whole-activity active summary |
| `INTERVAL_REST` | Rest intervals |

#### Split Summary Object Structure

```json
{
  "noOfSplits": 74,
  "totalAscent": 198.61,
  "duration": 8329.63,
  "splitType": "RWD_RUN",
  "numClimbSends": 0,
  "maxElevationGain": 38.09,
  "averageElevationGain": 2.13,
  "maxDistance": 2949,
  "distance": 21000.81,
  "averageSpeed": 2.52,
  "maxSpeed": 3.94,
  "numFalls": 0,
  "elevationLoss": 1466.33
}
```

| Field | Type | Unit | Notes |
|-------|------|------|-------|
| `noOfSplits` | number | count | Number of segments in this category |
| `splitType` | string | — | See table above |
| `duration` | number | seconds | Total time in this split type |
| `distance` | number | meters | Total distance |
| `totalAscent` | number | meters | |
| `elevationLoss` | number | meters | |
| `maxElevationGain` | number | meters | Largest single-segment elevation gain |
| `averageElevationGain` | number | meters | Average per segment |
| `maxDistance` | number | meters | Longest single segment |
| `averageSpeed` | number | m/s | |
| `maxSpeed` | number | m/s | |
| `numClimbSends` | number | count | Climbing-specific |
| `numFalls` | number | count | Climbing-specific |

### Pilates-Specific: Exercise Sets

Pilates activities contain `summarizedExerciseSets` (absent/empty for trail runs) and related fields:

| Field | Type | Notes |
|-------|------|-------|
| `totalSets` | number | e.g. `19` |
| `activeSets` | number | e.g. `19` |
| `summarizedExerciseSets` | array | Array of exercise objects |
| `workoutId` | number | Garmin workout template ID |

#### Exercise Set Object Example

```json
{
  "category": "MOVE",
  "subCategory": "MERMAID_STRETCH",
  "reps": 0,
  "volume": 0,
  "duration": 60000,
  "sets": 1,
  ...
}
```

### Device & Owner

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `manufacturer` | string | `"GARMIN"` | |
| `deviceId` | number | `3483859861` | |
| `ownerId` | number | `90568238` | Garmin user ID |
| `ownerFullName` | string | `"XD-DENG"` | |
| `ownerDisplayName` | string | `"26ebc362-..."` | UUID-style display name |
| `ownerProfileImageUrlSmall` | string | S3 URL | |
| `ownerProfileImageUrlMedium` | string | S3 URL | |
| `ownerProfileImageUrlLarge` | string | S3 URL | |
| `userPro` | boolean | `false` | |
| `userRoles` | array | `["SCOPE_GOLF_API_READ", ...]` | OAuth scopes |
| `privacy` | object | `{"typeId":3,"typeKey":"subscribers"}` | |
| `hasVideo` | boolean | `false` | |
| `hasImages` | boolean | `false` | |

### Other / Dive-Related (empty in this dataset)

| Field | Type | Notes |
|-------|------|-------|
| `summarizedDiveInfo` | object | `{"summarizedDiveGases":[]}` — always empty |
| `minActivityLapDuration` | number | Shortest lap in seconds |
| `hasSplits` | boolean | |

---

## Unit Summary

| Measurement | Unit |
|-------------|------|
| Distance | meters |
| Speed | m/s |
| Duration / Time-in-zone | seconds |
| Elevation | meters |
| Heart rate | BPM |
| Power | watts |
| Cadence | steps/min |
| Vertical oscillation | cm |
| Ground contact time | milliseconds |
| Stride length | cm |
| Calories | kcal |
| Water | mL |
| Fastest splits | seconds |
| Exercise set duration | milliseconds (note: different from activity duration) |
| Coordinates | decimal degrees (WGS84) |

---

## Null Pattern by Activity Type

Fields that are `null` for **all 10 pilates** activities but populated for **all 10 trail running** activities:

`elevationGain`, `elevationLoss`, `maxSpeed`, `startLatitude`, `startLongitude`, `avgPower`, `maxPower`, `normPower`, `avgVerticalOscillation`, `avgGroundContactTime`, `avgVerticalRatio`, `minElevation`, `maxElevation`, `maxVerticalSpeed`, `locationName`, `endLatitude`, `endLongitude`, `avgGradeAdjustedSpeed`, `fastestSplit_1000`, `fastestSplit_1609`, `fastestSplit_5000`, `fastestSplit_10000`, `powerTimeInZone_1–5`

Fields that are **sparse** (null in some trail runs too):

- `description` — null in 11/20 (only some activities have descriptions)
- `vO2MaxValue` — null in 11/20
- `avgElevation` — null in 19/20 (almost always null)
- `fastestSplit_21098` — null in 12/20 (only runs longer than half marathon distance)

---
---

## API 2: Single Activity Detail

```bash
curl 'https://connect.garmin.com/gc-api/activity-service/activity/{activityId}' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### File Format

- **Compression**: Brotli (same as API 1)
- **Underlying format**: JSON **object** (single activity, NOT an array)
- **Decompression**: Same methods as API 1 (see above)

### Key Differences from API 1 (Activity List)

| Aspect | API 1 (List) | API 2 (Detail) |
|--------|-------------|----------------|
| Endpoint | `activitylist-service/activities/search/activities` | `activity-service/activity/{id}` |
| Response shape | JSON **array** of flat activity objects | JSON **object** with nested DTOs |
| Field structure | Flat (e.g. `distance`, `averageHR`) | Nested (e.g. `summaryDTO.distance`, `summaryDTO.averageHR`) |
| Cadence field name | `averageRunningCadenceInStepsPerMinute` | `averageRunCadence` |
| UUID field | `activityUUID` (string) | `activityUUID.uuid` (nested object) |
| Extra fields | `sportTypeId`, `vO2MaxValue`, HR zone times, power zone times, fastest splits | `minHR`, `minPower`, `totalWork`, stamina fields, `averageMovingSpeed`, sensors, file format |
| Split summaries | Basic (distance, duration, elevation, speed) | Rich (includes per-split HR, cadence, power, running dynamics) |

---

### Data Structure Overview

The response is a single JSON object with these top-level sections:

```
{
  activityId, activityUUID, activityName, description,
  userProfileId, isMultiSportParent, locationName,
  activityTypeDTO: { ... },
  eventTypeDTO: { ... },
  accessControlRuleDTO: { ... },
  timeZoneUnitDTO: { ... },
  metadataDTO: { ... },
  summaryDTO: { ... },
  splitSummaries: [ ... ]
}
```

---

### Top-Level Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `activityId` | number | `21797148497` | Same as API 1 |
| `activityUUID` | object | `{"uuid": "c2cd7220-..."}` | Note: nested object, not a plain string |
| `activityName` | string | `"Huddart-Skyline-Purisima Redwoods - Trail Running"` | |
| `description` | string \| null | `"- Ran with Deliang\n- ..."` | Multi-line, may contain Chinese characters |
| `userProfileId` | number | `90568238` | Same as `ownerId` in API 1 |
| `isMultiSportParent` | boolean | `false` | |
| `locationName` | string | `"San Mateo County"` | Reverse-geocoded (at root level, not in summaryDTO) |

### `activityTypeDTO`

Same structure as API 1's `activityType`:

```json
{
  "typeId": 6,
  "typeKey": "trail_running",
  "parentTypeId": 1,
  "isHidden": false,
  "restricted": false,
  "trimmable": true
}
```

### `eventTypeDTO`

```json
{ "typeId": 9, "typeKey": "uncategorized", "sortOrder": 10 }
```

### `accessControlRuleDTO`

```json
{ "typeId": 3, "typeKey": "subscribers" }
```

### `timeZoneUnitDTO`

More detailed than API 1's `timeZoneId`:

```json
{
  "unitId": 121,
  "unitKey": "America/Los_Angeles",
  "factor": 0,
  "timeZone": "America/Los_Angeles"
}
```

---

### `metadataDTO`

Contains device info, user info, and various boolean flags.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `isOriginal` | boolean | `true` | |
| `deviceApplicationInstallationId` | number | `1005232` | |
| `fileFormat` | object | `{"formatId":7,"formatKey":"fit"}` | Activity file format |
| `associatedCourseId` | number \| null | `394036999` | Linked course |
| `lastUpdateDate` | string | `"2026-02-08T01:01:30.0"` | ISO datetime |
| `uploadedDate` | string | `"2026-02-07T21:19:56.0"` | ISO datetime |
| `hasPolyline` | boolean | `true` | GPS track exists |
| `hasChartData` | boolean | `true` | |
| `hasHrTimeInZones` | boolean | `true` | |
| `hasPowerTimeInZones` | boolean | `true` | |
| `hasRunPowerWindData` | boolean | `true` | |
| `runPowerWindDataEnabled` | boolean | `true` | |
| `hasSplits` | boolean | `true` | |
| `hasHeatMap` | boolean | `false` | |
| `personalRecord` | boolean | `false` | |
| `manualActivity` | boolean | `false` | |
| `autoCalcCalories` | boolean | `false` | |
| `favorite` | boolean | `false` | |
| `elevationCorrected` | boolean | `false` | |
| `trimmed` | boolean | `false` | |
| `gcj02` | boolean | `false` | Chinese coordinate system flag |
| `manufacturer` | string | `"GARMIN"` | |
| `lapCount` | number | `33` | |
| `hasIntensityIntervals` | boolean | `false` | |

#### `metadataDTO.sensors` (array)

```json
[{
  "serialNumber": 8,
  "sourceType": "BLUETOOTH_LOW_ENERGY",
  "bleDeviceType": "HEART_RATE",
  "batteryStatus": "NEW",
  "batteryLevel": 92
}]
```

#### `metadataDTO.userInfoDto`

Same user info as API 1 (`displayname`, `fullname`, profile image URLs, `userPro`).

#### `metadataDTO.deviceMetaDataDTO`

```json
{
  "deviceId": "3483859861",
  "deviceTypePk": 37073,
  "deviceVersionPk": 1005232
}
```

---

### `summaryDTO`

Contains all the numeric performance data. Most fields correspond to flat fields in API 1 but with some name differences and extra fields.

#### Time

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `startTimeLocal` | string | `"2026-02-07T07:54:30.0"` | ISO format (API 1 uses `"2026-02-07 07:54:30"` space-separated) |
| `startTimeGMT` | string | `"2026-02-07T15:54:30.0"` | ISO format |
| `duration` | number | `16398.176` | Seconds |
| `movingDuration` | number | `15937.093` | Seconds |
| `elapsedDuration` | number | `16398.176` | Seconds |

Note: No `endTimeGMT` or `beginTimestamp` — API 1 has those but API 2 does not.

#### Distance, Speed & Cadence

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `distance` | number | `32600.82` | Meters |
| `averageSpeed` | number | `1.988` | m/s |
| `maxSpeed` | number | `3.956` | m/s |
| `averageMovingSpeed` | number | `2.046` | m/s — **not in API 1** |
| `avgGradeAdjustedSpeed` | number | `2.322` | m/s |
| `steps` | number | `38894` | |
| `averageRunCadence` | number | `121.80` | Steps/min (API 1 calls this `averageRunningCadenceInStepsPerMinute`) |
| `maxRunCadence` | number | `219` | (API 1: `maxRunningCadenceInStepsPerMinute`) |

#### Elevation

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `elevationGain` | number | `1347.99` | Meters |
| `elevationLoss` | number | `1345.23` | Meters |
| `maxElevation` | number | `650.8` | Meters |
| `minElevation` | number | `142` | Meters |
| `avgElevation` | number | `378.42` | Meters — often null in API 1, present here |
| `maxVerticalSpeed` | number | `0.6` | m/s |

#### Heart Rate

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `averageHR` | number | `131` | BPM |
| `maxHR` | number | `166` | BPM |
| `minHR` | number | `82` | BPM — **not in API 1** |

Note: HR zone times (`hrTimeInZone_1` through `_5`) are **not** in this API's response. They exist only in API 1.

#### Power

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `averagePower` | number | `193` | Watts |
| `maxPower` | number | `499` | Watts |
| `minPower` | number | `0` | Watts — **not in API 1** |
| `normalizedPower` | number | `225` | Watts |
| `totalWork` | number | `753.93` | **not in API 1** — total work in kJ |

Note: Power zone times (`powerTimeInZone_1` through `_5`) are **not** in this API's response. They exist only in API 1.

#### Running Dynamics

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `groundContactTime` | number | `309.5` | Milliseconds (API 1: `avgGroundContactTime`) |
| `strideLength` | number | `86.67` | cm (API 1: `avgStrideLength`) |
| `verticalOscillation` | number | `7.28` | cm (API 1: `avgVerticalOscillation`) |
| `verticalRatio` | number | `8.57` | Percentage (API 1: `avgVerticalRatio`) |

#### Calories & Fitness

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `calories` | number | `2494` | kcal |
| `bmrCalories` | number | `386` | kcal |
| `waterEstimated` | number | `2927` | mL |

#### Training Effect & Load

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `trainingEffect` | number | `4` | API 1 calls this `aerobicTrainingEffect` |
| `anaerobicTrainingEffect` | number | `0` | |
| `aerobicTrainingEffectMessage` | string | `"HIGHLY_IMPROVING_AEROBIC_ENDURANCE_10"` | |
| `anaerobicTrainingEffectMessage` | string | `"NO_ANAEROBIC_BENEFIT_0"` | |
| `trainingEffectLabel` | string | `"AEROBIC_BASE"` | |
| `activityTrainingLoad` | number | `178.46` | |
| `moderateIntensityMinutes` | number | `89` | Minutes |
| `vigorousIntensityMinutes` | number | `175` | Minutes |
| `differenceBodyBattery` | number | `-30` | |

#### Stamina (not in API 1)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `beginPotentialStamina` | number | `99` | Stamina at start (0–100 scale) |
| `endPotentialStamina` | number | `47` | Stamina at end |
| `minAvailableStamina` | number | `47` | Lowest stamina during activity |

#### Location & GPS

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `startLatitude` | number | `37.432` | Decimal degrees |
| `startLongitude` | number | `-122.299` | Decimal degrees |
| `endLatitude` | number | `37.430` | Decimal degrees |
| `endLongitude` | number | `-122.299` | Decimal degrees |

#### Other

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `minActivityLapDuration` | number | `341.968` | Seconds |

---

### `splitSummaries` (Richer than API 1)

Same array structure as API 1, but each split object contains **additional per-split metrics** not available in API 1.

#### Split Types (same as API 1)

`RWD_RUN`, `RWD_WALK`, `RWD_STAND`, `INTERVAL_ACTIVE`, `INTERVAL_REST`

#### Extra Fields Per Split (not in API 1)

| Field | Type | Unit | Notes |
|-------|------|------|-------|
| `movingDuration` | number | seconds | Moving time within this split type |
| `averageMovingSpeed` | number | m/s | |
| `calories` | number | kcal | Per-split calories |
| `bmrCalories` | number | kcal | |
| `averageHR` | number | BPM | Per-split average HR |
| `maxHR` | number | BPM | Per-split max HR |
| `averageRunCadence` | number | steps/min | |
| `maxRunCadence` | number | steps/min | |
| `averagePower` | number | watts | |
| `maxPower` | number | watts | |
| `normalizedPower` | number | watts | |
| `groundContactTime` | number | ms | |
| `strideLength` | number | cm | |
| `verticalOscillation` | number | cm | |
| `verticalRatio` | number | % | |
| `totalExerciseReps` | number | count | |
| `avgVerticalSpeed` | number | m/s | |
| `avgGradeAdjustedSpeed` | number | m/s | |
| `maxDistanceWithPrecision` | number | meters | Higher-precision version of `maxDistance` |
| `avgStepFrequency` | number | steps/min | Same as `averageRunCadence` |
| `avgStepLength` | number | mm | Note: in **mm**, not cm |

---

### Fields in API 1 but NOT in API 2

These fields are available only via the activity list search endpoint:

- `sportTypeId`
- `beginTimestamp` (Unix ms)
- `endTimeGMT`
- `vO2MaxValue`
- `hrTimeInZone_1` through `hrTimeInZone_5`
- `powerTimeInZone_1` through `powerTimeInZone_5`
- `fastestSplit_1000`, `fastestSplit_1609`, `fastestSplit_5000`, `fastestSplit_10000`, `fastestSplit_21098`
- `maxDoubleCadence`
- `summarizedExerciseSets` (pilates)
- `totalSets`, `activeSets`, `workoutId`
- `summarizedDiveInfo`
- Owner profile fields (`ownerFullName`, `ownerDisplayName`, `ownerProfileImageUrlSmall/Medium/Large`, `userRoles`)

### Fields in API 2 but NOT in API 1

These fields are available only via the single activity detail endpoint:

- `minHR`, `minPower`
- `totalWork` (kJ)
- `averageMovingSpeed`
- `beginPotentialStamina`, `endPotentialStamina`, `minAvailableStamina`
- `metadataDTO.sensors` (BLE device info)
- `metadataDTO.fileFormat`
- `metadataDTO.associatedCourseId`
- `metadataDTO.uploadedDate`, `metadataDTO.lastUpdateDate`
- `timeZoneUnitDTO.unitKey` / `timeZoneUnitDTO.timeZone` (timezone name)
- Rich per-split metrics (HR, cadence, power, running dynamics per split type)

---
---

## API 3: Hill Score Stats (Daily Metrics)

```bash
curl 'https://connect.garmin.com/gc-api/metrics-service/metrics/hillscore/stats?startDate=2026-01-30&endDate=2026-02-26&aggregation=daily' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

This is a **different service** from APIs 1 & 2 (`metrics-service` vs `activity-service` / `activitylist-service`). It returns **daily time-series data** for Garmin's Hill Score feature, not per-activity data.

### Query Parameters

| Parameter | Example | Notes |
|-----------|---------|-------|
| `startDate` | `2026-01-30` | ISO date (YYYY-MM-DD) |
| `endDate` | `2026-02-26` | ISO date (YYYY-MM-DD) |
| `aggregation` | `daily` | Granularity of data points |

### File Format

- **Compression**: Brotli (same as APIs 1 & 2)
- **Underlying format**: JSON **object**
- **Decompression**: Same methods as API 1 (see above)

### Response Structure

```json
{
  "userProfilePK": 90568238,
  "startDate": "2026-01-30",
  "endDate": "2026-02-26",
  "periodAvgScore": { "2026-01-30": 73 },
  "maxScore": 74,
  "hillScoreDTOList": [ ... ]
}
```

### Top-Level Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | Same user ID as other APIs |
| `startDate` | string | `"2026-01-30"` | Echoes query param |
| `endDate` | string | `"2026-02-26"` | Echoes query param |
| `periodAvgScore` | object | `{"2026-01-30": 73}` | Average score for the period, keyed by start date |
| `maxScore` | number | `74` | Highest overall score in the period |

### `hillScoreDTOList` (Array of Daily Entries)

One entry per day in the date range, ordered newest-first (descending by date).

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | |
| `deviceId` | number | `3483859861` | Same device ID as in activity APIs |
| `calendarDate` | string | `"2026-02-26"` | ISO date |
| `overallScore` | number | `74` | Combined hill score (0–100 scale) |
| `strengthScore` | number | `36` | Hill strength component |
| `enduranceScore` | number | `79` | Hill endurance component |
| `hillScoreClassificationId` | number | `4` | Classification tier (always `4` in this dataset) |
| `hillScoreFeedbackPhraseId` | number | `32` | ID for feedback text, cycles through values 30–35 |
| `vo2Max` | number \| null | `null` | Always null in this dataset |
| `vo2MaxPreciseValue` | number \| null | `null` | Always null in this dataset |
| `primaryTrainingDevice` | boolean | `true` | Whether this is the primary device |

### Data Characteristics (from this 28-day sample)

- **28 daily entries** (one per day, 2026-01-30 to 2026-02-26)
- **Overall score range**: 71–74 (very stable)
- **Strength score range**: 32–37
- **Endurance score range**: 76–80
- Scores change gradually day-to-day (typically ±1)
- `hillScoreClassificationId` is consistently `4` (likely a tier label like "Good" or "Very Good")
- `hillScoreFeedbackPhraseId` cycles through 30–35 (6 distinct feedback phrases)
- `vo2Max` / `vo2MaxPreciseValue` are always null — VO2 max may be delivered via a separate API

### Relationship to Activity APIs

This API is **independent** of the activity APIs:
- Uses `metrics-service` (not `activity-service` or `activitylist-service`)
- Returns **daily aggregate metrics**, not per-activity data
- No `activityId` reference — scores are computed from training history, not tied to individual activities
- Shares `userProfilePK` and `deviceId` identifiers with activity APIs

---
---

## API 4: Endurance Score Stats (Weekly Metrics)

```bash
curl 'https://connect.garmin.com/gc-api/metrics-service/metrics/endurancescore/stats?startDate=2025-12-06&endDate=2026-02-27&aggregation=weekly' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Same `metrics-service` as API 3 (Hill Score), but for Garmin's **Endurance Score** feature. Returns **weekly time-series data** with score breakdowns by activity type and training group. Unlike Hill Score (0–100 scale), Endurance Score uses a **larger numeric scale** (roughly 3,500–10,500+).

### Query Parameters

| Parameter | Example | Notes |
|-----------|---------|-------|
| `startDate` | `2025-12-06` | ISO date (YYYY-MM-DD) |
| `endDate` | `2026-02-27` | ISO date (YYYY-MM-DD) |
| `aggregation` | `weekly` | Granularity — `weekly` groups by week start date (also supports `daily`) |

### Response Structure

```json
{
  "userProfilePK": 90568238,
  "startDate": "2025-12-06",
  "endDate": "2026-02-27",
  "avg": 7237,
  "max": 7486,
  "groupMap": { "<week-start-date>": { ... }, ... },
  "enduranceScoreDTO": { ... }
}
```

### Top-Level Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | Same user ID as other APIs |
| `startDate` | string | `"2025-12-06"` | Echoes query param |
| `endDate` | string | `"2026-02-27"` | Echoes query param |
| `avg` | number | `7237` | Period average endurance score |
| `max` | number | `7486` | Period maximum endurance score |

### `groupMap` (Weekly Entries)

Keyed by week start date (ISO date string). One entry per week in the date range.

#### Weekly Group Object

```json
{
  "groupAverage": 7306,
  "groupMax": 7346,
  "enduranceContributorDTOList": [
    { "activityTypeId": 225, "group": null, "contribution": 7.43 },
    { "activityTypeId": 3, "group": null, "contribution": 8.01 },
    { "activityTypeId": null, "group": 0, "contribution": 76.76 },
    { "activityTypeId": null, "group": 8, "contribution": 7.81 }
  ]
}
```

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `groupAverage` | number | `7306` | Average endurance score for the week |
| `groupMax` | number | `7346` | Max endurance score for the week |
| `enduranceContributorDTOList` | array | See below | Breakdown of contributing factors |

#### `enduranceContributorDTOList` Entry

Each entry represents either an activity type or a training group contributing to the score. Exactly one of `activityTypeId` or `group` is non-null.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `activityTypeId` | number \| null | `225` | Garmin activity type ID (null when `group` is set) |
| `group` | number \| null | `0` | Training group ID (null when `activityTypeId` is set) |
| `contribution` | number | `76.76` | Percentage contribution to the score |

##### Known `activityTypeId` Values

| `activityTypeId` | Likely Meaning |
|-------------------|---------------|
| `225` | Walking / casual activity |
| `3` | Running (road running; distinct from trail running typeId 6 in activity APIs) |

##### Known `group` Values

| `group` | Likely Meaning |
|---------|---------------|
| `0` | Low-intensity / baseline activity (largest contributor, ~73–79%) |
| `8` | High-intensity activity (~4–8%) |

### `enduranceScoreDTO` (Current Day Snapshot)

A single object representing the most recent day's endurance score with classification info.

```json
{
  "userProfilePK": 90568238,
  "deviceId": 3483859861,
  "calendarDate": "2026-02-27",
  "overallScore": 7460,
  "classification": 5,
  "feedbackPhrase": 78,
  "primaryTrainingDevice": true,
  "gaugeLowerLimit": 3570,
  "classificationLowerLimitIntermediate": 5100,
  "classificationLowerLimitTrained": 5800,
  "classificationLowerLimitWellTrained": 6600,
  "classificationLowerLimitExpert": 7300,
  "classificationLowerLimitSuperior": 8100,
  "classificationLowerLimitElite": 8800,
  "gaugeUpperLimit": 10560,
  "contributors": [ ... ]
}
```

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | |
| `deviceId` | number | `3483859861` | Same device as other APIs |
| `calendarDate` | string | `"2026-02-27"` | Date of this snapshot |
| `overallScore` | number | `7460` | Current endurance score |
| `classification` | number | `5` | Classification tier (see scale below) |
| `feedbackPhrase` | number | `78` | ID for feedback text |
| `primaryTrainingDevice` | boolean | `true` | |

#### Classification Scale (Gauge Thresholds)

| Field | Value | Tier |
|-------|-------|------|
| `gaugeLowerLimit` | 3570 | Minimum gauge value |
| `classificationLowerLimitIntermediate` | 5100 | Intermediate |
| `classificationLowerLimitTrained` | 5800 | Trained |
| `classificationLowerLimitWellTrained` | 6600 | Well Trained |
| `classificationLowerLimitExpert` | 7300 | Expert |
| `classificationLowerLimitSuperior` | 8100 | Superior |
| `classificationLowerLimitElite` | 8800 | Elite |
| `gaugeUpperLimit` | 10560 | Maximum gauge value |

With a current score of 7460 and `classification: 5`, the user falls in the **Expert** tier (7300–8099).

#### `contributors` (Current Day)

Same structure as `enduranceContributorDTOList` in weekly groups, showing today's contribution breakdown:

| Contributor | Contribution |
|-------------|-------------|
| group `0` (low-intensity baseline) | 79.25% |
| activityTypeId `225` (walking) | 9.65% |
| activityTypeId `3` (running) | 6.38% |
| group `8` (high-intensity) | 4.72% |

### Data Characteristics (from this 12-week sample: 2025-12-06 to 2026-02-27)

- **12 weekly entries** in `groupMap`
- **Weekly average score range**: 7037–7452 (gradual upward trend)
- **Weekly max score range**: 7088–7486
- **Period average**: 7237, **Period max**: 7486
- Scores dipped mid-January (~7037) then recovered to ~7452 by late February
- Low-intensity baseline (group `0`) is consistently the dominant contributor (~73–79%)
- Running contribution (activityTypeId `3`) peaked mid-January (~14.6%) then declined
- Walking contribution (activityTypeId `225`) gradually increased over the period (~7.0 → 10.0%)

### Relationship to Other APIs

- Same `metrics-service` as API 3 (Hill Score) — sibling endpoint (`endurancescore` vs `hillscore`)
- Uses the same `userProfilePK` and `deviceId` identifiers
- Hill Score has `overallScore`, `strengthScore`, `enduranceScore` components (0–100 scale)
- Endurance Score has a single `overallScore` with contribution breakdowns (larger numeric scale ~3500–10500)
- Both are daily aggregate metrics independent of individual activities

---
---

## API 5: Sleep Stats (Daily, and allow fetching multiple days)

```bash
curl 'https://connect.garmin.com/gc-api/sleep-service/stats/sleep/daily/2026-02-21/2026-02-27' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.3 Safari/605.1.15' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Uses `sleep-service` (distinct from `metrics-service` and `activity-service`). Returns daily sleep summaries for a date range: one aggregate `overallStats` object for the period plus per-night `individualStats`. Unlike the activity APIs, dates are **path parameters** (not query params).

### Path Parameters

| Parameter | Example | Notes |
|-----------|---------|-------|
| `{startDate}` | `2026-02-21` | ISO date (YYYY-MM-DD), inclusive |
| `{endDate}` | `2026-02-27` | ISO date (YYYY-MM-DD), inclusive |

### File Format

- **Compression**: Brotli (same as APIs 1–4)
- **Underlying format**: JSON **object**
- **Decompression**: Same Node.js method as API 1

### Response Structure

```json
{
  "overallStats": { ... },
  "individualStats": [ { "calendarDate": "2026-02-21", "values": { ... } }, ... ]
}
```

---

### `overallStats` (Period Aggregate)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `averageSleepScore` | number | `73.0` | Average sleep score across the period (0–100) |
| `averageSleepSeconds` | number | `25286.0` | Average total sleep duration in **seconds** |
| `averageSleepNeed` | number | `496.0` | Average sleep need in **minutes** |
| `averageLocalSleepStartTime` | number | `-4208.0` | Average sleep start time as **seconds from midnight** of the `calendarDate`; negative = before midnight (e.g. -4208s ≈ 22:50 PM) |
| `averageLocalSleepEndTime` | number | `22569.0` | Average sleep end time as **seconds from midnight** of the `calendarDate` (e.g. 22569s ≈ 6:16 AM) |
| `averageRestingHeartRate` | number | `52.0` | BPM |
| `meanAvgHeartRate` | number | `56.0` | Average of per-night average HR, in BPM |
| `averageSpO2` | number | `97.0` | Average blood oxygen, % |
| `averageRespiration` | number | `13.0` | Average breaths per minute |
| `averageBodyBatteryChange` | number | `52.0` | Average body battery gained per night |
| `averageSkinTempF` | number | `0.0` | Average skin temperature delta from baseline in **°F** |
| `averageSkinTempC` | number | `0.0` | Average skin temperature delta from baseline in **°C** |

---

### `individualStats` (Array of Nightly Entries)

One entry per calendar date in the range, ordered oldest-first. Each entry has:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `calendarDate` | string | `"2026-02-21"` | The **wake-up date** (not the date sleep started) |
| `values` | object | See below | All nightly metrics |

#### `values` Object

##### Sleep Duration & Stages

All times are in **seconds**.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `totalSleepTimeInSeconds` | number | `25140` | Total sleep = `remTime + deepTime + lightTime` (awake time excluded) |
| `remTime` | number | `2460` | REM sleep |
| `deepTime` | number | `6720` | Deep sleep |
| `lightTime` | number | `15960` | Light sleep |
| `awakeTime` | number | `1560` | Awake time during the sleep session (not counted in `totalSleepTimeInSeconds`) |
| `sleepNeed` | number | `470` | Sleep need in **minutes** |

**Invariant**: `totalSleepTimeInSeconds == remTime + deepTime + lightTime`

##### Sleep Timing

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `localSleepStartTimeInMillis` | number | `1771626909000` | Unix ms — local clock time encoded as if UTC (add UTC offset to get true UTC) |
| `localSleepEndTimeInMillis` | number | `1771653609000` | Unix ms — local clock time encoded as if UTC |
| `gmtSleepStartTimeInMillis` | number | `1771655709000` | Unix ms — true UTC timestamp |
| `gmtSleepEndTimeInMillis` | number | `1771682409000` | Unix ms — true UTC timestamp |

Note: `gmtSleepStartTimeInMillis - localSleepStartTimeInMillis = UTC offset in ms` (28,800,000 ms = 8 hours for PST/UTC-8).

##### Sleep Score & Quality

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `sleepScore` | number | `71` | Overall sleep score (0–100) |
| `sleepScoreQuality` | string | `"FAIR"` | Qualitative tier: `"POOR"`, `"FAIR"`, `"GOOD"` (higher tiers like `"EXCELLENT"` may exist) |

##### Heart Rate & HRV

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `avgHeartRate` | number | `59.0` | Average overnight HR, BPM |
| `restingHeartRate` | number | `54` | Resting HR, BPM |
| `avgOvernightHrv` | number | `31.0` | Average overnight HRV (ms) |
| `hrv7dAverage` | number | `37.0` | 7-day rolling HRV average (ms) |
| `hrvStatus` | string | `"BALANCED"` | HRV status label: `"BALANCED"`, `"UNBALANCED"`, `"LOW"` |

##### Biometrics

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `spO2` | number | `97.48` | Blood oxygen percentage |
| `respiration` | number | `13.7` | Breaths per minute |
| `skinTempF` | number | `0.5` | Skin temperature delta from personal baseline in **°F** |
| `skinTempC` | number | `0.3` | Skin temperature delta from personal baseline in **°C** |
| `bodyBatteryChange` | number | `39` | Body battery gained during sleep |

---

### Data Summary (7-night sample: 2026-02-21 to 2026-02-27)

| Date | Score | Quality | Total Sleep | REM | Deep | Light | Awake | Avg HR | HRV | SpO2 |
|------|-------|---------|-------------|-----|------|-------|-------|--------|-----|------|
| 2026-02-21 | 71 | FAIR | 6h 59m | 41m | 1h 52m | 4h 26m | 26m | 59 | 31 | 97.5% |
| 2026-02-22 | 47 | POOR | 6h 30m | 0m | 1h 18m | 5h 12m | 52m | 61 | 28 | 97.1% |
| 2026-02-23 | 86 | GOOD | 7h 43m | 1h 33m | 2h 03m | 4h 07m | 10m | 56 | 36 | 98.0% |
| 2026-02-24 | 79 | FAIR | 6h 51m | 1h 12m | 2h 05m | 3h 34m | 20m | 55 | 37 | 96.8% |
| 2026-02-25 | 77 | FAIR | 7h 10m | 47m | 2h 07m | 4h 16m | 26m | 53 | 45 | 97.5% |
| 2026-02-26 | 78 | FAIR | 7h 06m | 1h 02m | 2h 03m | 4h 01m | 19m | 54 | 40 | 97.3% |
| 2026-02-27 | 72 | FAIR | 6h 51m | 39m | 1h 41m | 4h 31m | 21m | 56 | 37 | 97.7% |
| **Avg** | **73** | — | **7h 01m** | **52m** | **1h 54m** | **4h 18m** | **25m** | **56** | **36** | **97.0%** |

**Key observations from this sample:**
- Sleep starts consistently ~22:45–23:05 local time; wake ~06:00–06:40
- Sleep need (~496 min = 8.27h) exceeds actual sleep (~421 min = 7.02h) every night
- Feb 22 is an outlier: score 47 (POOR), no REM detected, high awake time (52m), low HRV (28)
- Feb 23 is the best night: score 86 (GOOD), highest REM (1h 33m), most total sleep (7h 43m)
- HRV ranges 28–45 ms; `hrv7dAverage` is stable (35–37), suggesting HRV fluctuates but 7-day trend is steady
- Skin temp delta ranges from -0.6°F to +0.5°F (small nightly variation around personal baseline)
- `bodyBatteryChange` correlates with sleep score (33 on poor night vs 59–64 on good nights)

### Relationship to Other APIs

- Uses `sleep-service` (unique to this API — not `activity-service`, `activitylist-service`, or `metrics-service`)
- Shares `calendarDate` key with API 3 (Hill Score daily entries)
- `bodyBatteryChange` during sleep complements `differenceBodyBattery` from activity APIs (which captures battery *lost* during a workout)
- No `activityId` reference — sleep is tracked independently of exercise activities
- `restingHeartRate` here is the nightly value; activity APIs report HR only during activity windows

---
---

## API 6: Daily Sleep Detail (Single Night, Full Time-Series)

```bash
curl 'https://connect.garmin.com/gc-api/sleep-service/sleep/dailySleepData?date=2026-02-26&nonSleepBufferMinutes=60' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.3 Safari/605.1.15' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Same `sleep-service` as API 5, but a **different sub-endpoint** (`sleep/dailySleepData` vs `stats/sleep/daily`). Returns a single night's full detail: a rich summary DTO plus **seven time-series arrays** (movement, sleep stages, SpO2, heart rate, stress, body battery, HRV, respiration). API 5 gives multi-day summary rows; this API gives the full signal data for one night.

### Query Parameters

| Parameter | Example | Notes |
|-----------|---------|-------|
| `date` | `2026-02-26` | The **wake-up date** (ISO YYYY-MM-DD), same convention as `calendarDate` in API 5 |
| `nonSleepBufferMinutes` | `60` | Minutes of pre/post-sleep data to include in time-series arrays (default unknown; 60 observed) |

### File Format

- **Compression**: Brotli (same as APIs 1–5)
- **Underlying format**: JSON **object**
- **Compressed size**: ~14.9 KB; **Decompressed size**: ~182 KB (much larger than API 5 due to time-series)

### Response Structure

```
{
  dailySleepDTO:                         // main summary object
  sleepMovement:                         // 1-min movement signal (array)
  remSleepData:                          // boolean: REM available
  sleepLevels:                           // sleep stage segments (array)
  sleepRestlessMoments:                  // restless event timestamps (array)
  restlessMomentsCount:                  // integer count
  wellnessSpO2SleepSummaryDTO:           // SpO2 summary object
  wellnessEpochSPO2DataDTOList:          // 1-min SpO2 readings (array)
  wellnessEpochRespirationDataDTOList:   // ~2-min respiration readings (array)
  wellnessEpochRespirationAveragesList:  // hourly respiration averages (array)
  respirationVersion:                    // integer
  sleepHeartRate:                        // 2-min HR readings (array)
  sleepStress:                           // 3-min stress scores (array)
  sleepBodyBattery:                      // 3-min body battery values (array)
  skinTempDataExists:                    // boolean
  hrvData:                               // 5-min HRV readings (array)
  breathingDisruptionData:               // breathing disruption segments (array)
  avgSkinTempDeviationC:                 // scalar float
  avgSkinTempDeviationF:                 // scalar float
  avgOvernightHrv:                       // scalar integer
  hrvStatus:                             // scalar string
  bodyBatteryChange:                     // scalar integer
  skinTempCalibrationDays:               // scalar integer
  restingHeartRate:                      // scalar integer
}
```

---

### `dailySleepDTO`

#### Identity & Window

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `1772088847000` | Same value as `sleepStartTimestampGMT` |
| `userProfilePK` | number | `90568238` | Same user ID as other APIs |
| `calendarDate` | string | `"2026-02-26"` | Wake-up date (not sleep-start date) |
| `sleepWindowConfirmed` | boolean | `true` | Whether window was auto-confirmed |
| `sleepWindowConfirmationType` | string | `"enhanced_confirmed_final"` | Confirmation method |
| `sleepFromDevice` | boolean | `true` | Whether recorded by wearable |
| `retro` | boolean | `false` | Retroactively detected sleep |
| `deviceRemCapable` | boolean | `true` | Whether device tracks REM |
| `sleepVersion` | number | `2` | Algorithm version |
| `ageGroup` | string | `"ADULT"` | Used for age-adjusted score targets |
| `autoSleepStartTimestampGMT` | number \| null | `null` | Auto-detected window (null when confirmed) |
| `autoSleepEndTimestampGMT` | number \| null | `null` | |
| `sleepQualityTypePK` | null | `null` | Always null in this dataset |
| `sleepResultTypePK` | null | `null` | Always null in this dataset |

#### Timestamps (same semantics as API 5)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `sleepStartTimestampGMT` | number | `1772088847000` | Unix ms, true UTC |
| `sleepEndTimestampGMT` | number | `1772115547000` | Unix ms, true UTC |
| `sleepStartTimestampLocal` | number | `1772060047000` | Unix ms, local time encoded as if UTC |
| `sleepEndTimestampLocal` | number | `1772086747000` | Unix ms, local time encoded as if UTC |

#### Sleep Durations

All in **seconds**.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `sleepTimeSeconds` | number | `25560` | Total sleep (same as API 5 `totalSleepTimeInSeconds`) |
| `napTimeSeconds` | number | `1440` | Total nap time for the day |
| `deepSleepSeconds` | number | `7380` | |
| `lightSleepSeconds` | number | `14460` | |
| `remSleepSeconds` | number | `3720` | |
| `awakeSleepSeconds` | number | `1140` | |
| `unmeasurableSleepSeconds` | number | `0` | Time device couldn't measure |

#### Vitals Summary

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `avgHeartRate` | number | `54` | BPM overnight average |
| `averageSpO2Value` | number | `97` | Blood oxygen % (average) |
| `lowestSpO2Value` | number | `84` | Min SpO2 — **not in API 5** |
| `highestSpO2Value` | number | `100` | Max SpO2 — **not in API 5** |
| `averageSpO2HRSleep` | number | `54` | Avg HR during SpO2 measurement window |
| `averageRespirationValue` | number | `12` | Breaths/min (average) |
| `lowestRespirationValue` | number | `10` | Min respiration — **not in API 5** |
| `highestRespirationValue` | number | `17` | Max respiration — **not in API 5** |
| `awakeCount` | number | `2` | Number of distinct awake episodes — **not in API 5** |
| `avgSleepStress` | number | `18` | Average stress score during sleep — **not in API 5** |
| `breathingDisruptionSeverity` | string | `"NONE"` | Breathing disruption level — **not in API 5** |

#### Sleep Score & Feedback

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `sleepScoreFeedback` | string | `"POSITIVE_LONG_AND_DEEP"` | Short feedback key — **not in API 5** |
| `sleepScoreInsight` | string | `"POSITIVE_EXERCISE"` | Insight key (e.g. exercise contributed positively) — **not in API 5** |
| `sleepScorePersonalizedInsight` | string | `"RHYTHM_POS_FAIR_OR_POOR_SLEEP_EXCELLENT_TIMING"` | More specific insight — **not in API 5** |

#### `sleepScores` (Component Breakdown — not in API 5)

An object with 7 scored sub-components, each including a `qualifierKey` and optimal ranges:

| Component | Fields | Example Values |
|-----------|--------|----------------|
| `overall` | `value`, `qualifierKey` | `78`, `"FAIR"` |
| `totalDuration` | `qualifierKey`, `optimalStart`, `optimalEnd` (seconds) | `"GOOD"`, `28200`, `28200` |
| `deepPercentage` | `value` (%), `qualifierKey`, `optimalStart/End` (%), `idealStartInSeconds`, `idealEndInSeconds` | `29%`, `"EXCELLENT"`, `16–33%` |
| `remPercentage` | same as deepPercentage | `15%`, `"FAIR"`, `21–31%` |
| `lightPercentage` | same as deepPercentage | `57%`, `"EXCELLENT"`, `30–64%` |
| `stress` | `qualifierKey`, `optimalStart/End` (stress score) | `"FAIR"`, `0–15` |
| `awakeCount` | `qualifierKey`, `optimalStart/End` (count) | `"FAIR"`, `0–1` |
| `restlessness` | `qualifierKey`, `optimalStart/End` (count) | `"FAIR"`, `0–5` |

`qualifierKey` values: `"EXCELLENT"`, `"GOOD"`, `"FAIR"`, `"POOR"` (same scale as API 5 `sleepScoreQuality`)

#### `sleepNeed` & `nextSleepNeed` (not in API 5)

Both have identical structure — `sleepNeed` is tonight's need, `nextSleepNeed` is tomorrow's projected need.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePk` | number | `90568238` | |
| `calendarDate` | string | `"2026-02-26"` | |
| `deviceId` | number | `3483859861` | |
| `timestampGmt` | string | `"2026-02-25T16:45:07"` | When this need was computed |
| `baseline` | number | `470` | Base sleep need in **minutes** (no adjustments) |
| `actual` | number | `490` | Adjusted sleep need in **minutes** — this is the `sleepNeed` value in API 5 |
| `feedback` | string | `"INCREASED"` | Direction of adjustment: `"INCREASED"`, `"NO_CHANGE_BALANCED"`, etc. |
| `trainingFeedback` | string | `"CHRONIC"` | Training load type contributing to need |
| `sleepHistoryAdjustment` | string | `"NO_CHANGE"` | Whether recent sleep history raised/lowered need |
| `hrvAdjustment` | string | `"INCREASING"` | HRV trend effect on need |
| `napAdjustment` | string | `"NO_CHANGE"` | Whether today's nap reduced need |
| `displayedForTheDay` | boolean | `true` | Whether shown in the app |
| `preferredActivityTracker` | boolean | `true` | Whether this device is primary |

#### `dailyNapDTOS` (Array — not in API 5)

One entry per nap detected during the day.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | |
| `deviceId` | number | `3483859861` | |
| `calendarDate` | string | `"2026-02-26"` | |
| `napTimeSec` | number | `1440` | Nap duration in **seconds** (1440s = 24 min) |
| `napStartTimestampGMT` | string | `"2026-02-26T18:27:10"` | ISO datetime, UTC |
| `napEndTimestampGMT` | string | `"2026-02-26T18:51:10"` | ISO datetime, UTC |
| `napFeedback` | string | `"IDEAL_TIMING_IDEAL_DURATION_LOW_NEED"` | Qualitative nap assessment |
| `napSource` | number | `0` | Detection source (0 = device) |
| `napStartTimeOffset` | number | `-480` | UTC offset in minutes at nap start (-480 = UTC-8, PST) |
| `napEndTimeOffset` | number | `-480` | |

---

### Time-Series Arrays

All arrays cover the sleep window plus `nonSleepBufferMinutes` (60 min) before and after if available.

#### `sleepMovement` — 1-minute resolution (565 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | string | ISO datetime, UTC (`"2026-02-26T05:54:00.0"`) |
| `endGMT` | string | ISO datetime, UTC |
| `activityLevel` | number | Continuous float movement intensity (e.g. `6.18`, `5.90`) |

#### `sleepLevels` — Variable-duration segments (21 items)

Segments covering the entire sleep session. Consecutive segments are contiguous.

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | string | ISO datetime, UTC |
| `endGMT` | string | ISO datetime, UTC |
| `activityLevel` | number | Sleep stage integer: see encoding below |

**`activityLevel` encoding (confirmed by summing segment durations vs `dailySleepDTO` stage totals):**

| Value | Stage |
|-------|-------|
| `0` | Deep sleep |
| `1` | Light sleep |
| `2` | REM sleep |
| `3` | Awake |

#### `sleepRestlessMoments` — Event list (44 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms (note: integer ms, unlike most other arrays which use ISO strings) |
| `value` | number | Always `1` — binary event marker |

`restlessMomentsCount` (top-level scalar) = `44` = `sleepRestlessMoments.length`

#### `sleepHeartRate` — 2-minute resolution (223 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms |
| `value` | number | Heart rate in BPM |

#### `sleepStress` — 3-minute resolution (149 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms |
| `value` | number | Stress score (0–100 scale) |

#### `sleepBodyBattery` — 3-minute resolution (149 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms |
| `value` | number | Body battery level (0–100 scale) |

Note: `sleepStress` and `sleepBodyBattery` have identical intervals and item counts, suggesting they share the same epoch grid.

#### `hrvData` — 5-minute resolution (89 items)

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms |
| `value` | number | HRV in ms |

#### `wellnessEpochSPO2DataDTOList` — 1-minute resolution (421 items)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePK` | number | `90568238` | |
| `deviceId` | number | `3483859861` | |
| `epochTimestamp` | string | `"2026-02-26T06:55:00.0"` | ISO datetime, UTC — start of epoch |
| `epochDuration` | number | `60` | Epoch duration in **seconds** (always 60) |
| `calendarDate` | string | `"2026-02-25T00:00:00.0"` | Local date of sleep start (UTC-8 = Feb 25 for a Feb 26 wake-up) |
| `spo2Reading` | number | `98` | Blood oxygen % |
| `readingConfidence` | number | `7` | Quality metric (higher = more confident) |

Note: `calendarDate` in SpO2 entries reflects the **local date when sleep started** (night before the wake-up date), not the wake-up calendarDate.

#### `wellnessEpochRespirationDataDTOList` — ~2-minute resolution (223 items)

| Field | Type | Notes |
|-------|------|-------|
| `startTimeGMT` | number | Unix ms |
| `respirationValue` | number | Breaths per minute (integer) |

#### `wellnessEpochRespirationAveragesList` — Hourly averages (9 items)

One entry per clock-hour boundary covered by the sleep window. First and last entries may be partial-hour and have `respirationAverageValue = -2` (sentinel for invalid/insufficient data).

| Field | Type | Notes |
|-------|------|-------|
| `epochEndTimestampGmt` | number | Unix ms — end of the 1-hour bucket |
| `respirationAverageValue` | number | Avg breaths/min for the hour, or `-2` if invalid |
| `respirationHighValue` | number \| null | Max breaths/min in the hour (null when average is -2) |
| `respirationLowValue` | number \| null | Min breaths/min in the hour (null when average is -2) |

#### `breathingDisruptionData` — Segments (4 items)

Covers the full sleep window in contiguous segments.

| Field | Type | Notes |
|-------|------|-------|
| `startGMT` | number | Unix ms |
| `endGMT` | number | Unix ms |
| `value` | number | `0` = no disruption, `1` = disruption present |

#### `wellnessSpO2SleepSummaryDTO`

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `userProfilePk` | number | `90568238` | |
| `deviceId` | number | `3483859861` | |
| `sleepMeasurementStartGMT` | string | `"2026-02-26T06:55:00.0"` | ISO datetime, UTC — SpO2 window start (≈ sleep start) |
| `sleepMeasurementEndGMT` | string | `"2026-02-26T14:19:00.0"` | ISO datetime, UTC — SpO2 window end (≈ sleep end) |
| `averageSPO2` | number | `97` | Average SpO2 % |
| `averageSpO2HR` | number | `54` | Average HR during SpO2 window, BPM |
| `lowestSPO2` | number | `84` | Minimum SpO2 detected |
| `alertThresholdValue` | null | `null` | SpO2 alert threshold (if configured) |
| `numberOfEventsBelowThreshold` | null | `null` | |
| `durationOfEventsBelowThreshold` | null | `null` | |

---

### Top-Level Scalar Fields

These match (and cross-validate with) the corresponding fields in API 5's `individualStats.values`:

| Field | Type | Example | API 5 equivalent |
|-------|------|---------|-----------------|
| `avgOvernightHrv` | number | `40` | `avgOvernightHrv` |
| `hrvStatus` | string | `"UNBALANCED"` | `hrvStatus` |
| `bodyBatteryChange` | number | `61` | `bodyBatteryChange` |
| `restingHeartRate` | number | `51` | `restingHeartRate` |
| `avgSkinTempDeviationC` | number | `-0.3` | `skinTempC` |
| `avgSkinTempDeviationF` | number | `-0.6` | `skinTempF` |
| `skinTempDataExists` | boolean | `true` | (indicates `skinTempC/F` are valid) |
| `skinTempCalibrationDays` | number | `19` | **not in API 5** — days used for baseline calibration |
| `remSleepData` | boolean | `true` | (indicates REM data present) |
| `restlessMomentsCount` | number | `44` | **not in API 5** |
| `respirationVersion` | number | `200` | **not in API 5** — algorithm version |

---

### Relationship to API 5

| Aspect | API 5 (Stats) | API 6 (Detail) |
|--------|--------------|----------------|
| Endpoint | `stats/sleep/daily/{start}/{end}` | `sleep/dailySleepData?date={date}` |
| Scope | Multi-day summary | Single night full detail |
| Time-series | None | 7 signal arrays (HR, HRV, SpO2, stress, body battery, respiration, movement) |
| Sleep stages | Total seconds per stage | Segment-level timeline + total seconds |
| SpO2 | Average only | Average, min, max, + per-minute readings |
| Respiration | Average only | Average, min, max, + per-epoch readings + hourly averages |
| Sleep score | Score + quality tier | Score + 7-component breakdown with optimal ranges + 3 feedback phrases |
| Sleep need | `actual` value only | Full breakdown: baseline, adjustments (HRV, training, nap, sleep history) |
| Nap data | None | Full nap DTOs with timing and feedback |
| Breathing | None | Disruption segments + severity |
| Response size | ~900 bytes compressed | ~14.9 KB compressed (~17× larger) |

---
---

## API 7: Monthly Calendar (All Item Types)

```bash
curl 'https://connect.garmin.com/gc-api/calendar-service/year/{year}/month/{month}' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Uses `calendar-service` (distinct from all other services). Returns a **monthly calendar view** containing all user items for a given month: activities, goals, notes, weight entries, naps, and events. This is likely the data source for Garmin Connect's calendar page. Unlike the activity list API (API 1), this returns **all item types** in a single response, not just activities.

### Path Parameters

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `{year}` | number | `2026` | Calendar year |
| `{month}` | number | `0` | **0-indexed** month: `0` = January, `1` = February, ..., `11` = December |

### File Format

- **Compression**: Brotli (same as APIs 1–6)
- **Underlying format**: JSON **object**
- **Decompression**: Same methods as API 1

### Response Structure

```json
{
  "startDayOfMonth": 4,
  "numOfDaysInMonth": 31,
  "numOfDaysInPrevMonth": 31,
  "month": 0,
  "year": 2026,
  "calendarItems": [ ... ]
}
```

### Top-Level Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `startDayOfMonth` | number | `4` | Day of week the 1st falls on: `0` = Sunday, `1` = Monday, ..., `6` = Saturday (Jan 1, 2026 = Thursday = `4`) |
| `numOfDaysInMonth` | number | `31` | Days in this month |
| `numOfDaysInPrevMonth` | number | `31` | Days in the previous month (for calendar grid rendering) |
| `month` | number | `0` | Echoes the 0-indexed month parameter |
| `year` | number | `2026` | Echoes the year parameter |

### `calendarItems` Array

A flat array of **all** calendar items for the month (plus a few days from adjacent months for calendar grid padding). Each item has a shared schema with many nullable fields — only the fields relevant to that `itemType` are populated.

#### Item Types

| `itemType` | Description | Count (3-month sample) |
|------------|-------------|------------------------|
| `activity` | Recorded activities (running, hiking, strength, etc.) | 167 |
| `goal` | Training goals with start/end markers | 19 |
| `weight` | Body weight measurements | 17 |
| `nap` | Detected nap sessions | 6 |
| `note` | User-created text notes | 6 |
| `event` | Scheduled races / events | 1 |

---

### Shared Calendar Item Schema

Every item has all fields below. Most are `null` for any given `itemType`. Fields are listed once; see per-type sections for which are populated.

```
id, groupId, trainingPlanId, itemType, activityTypeId, wellnessActivityUuid,
title, date, duration, distance, calories, floorsClimbed, avgRespirationRate,
unitOfPoolLength, weight, difference, courseId, courseName, sportTypeKey, url,
isStart, isRace, recurrenceId, isParent, parentId, userBadgeId,
badgeCategoryTypeId, badgeCategoryTypeDesc, badgeAwardedDate, badgeViewed,
hideBadge, startTimestampLocal, eventTimeLocal, diveNumber, maxDepth, avgDepth,
surfaceInterval, elapsedDuration, lapCount, bottomTime, atpPlanId, workoutId,
protectedWorkoutSchedule, activeSets, strokes, noOfSplits, maxGradeValue,
totalAscent, differenceStress, climbDuration, maxSpeed, averageHR,
activeSplitSummaryDuration, activeSplitSummaryDistance, maxSplitDistance,
maxSplitSpeed, location, shareableEventUuid, splitSummaryMode, completionTarget,
workoutUuid, napStartTimeLocal, beginPackWeight, hasSplits, maxPackWeight,
shareableEvent, phasedTrainingPlan, autoCalcCalories, decoDive, primaryEvent, subscribed
```

---

### Item Type: `activity`

The most common item type. Contains summary metrics for each recorded activity.

#### Always-Present Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `21349357653` | Activity ID (same as `activityId` in APIs 1 & 2) |
| `itemType` | string | `"activity"` | |
| `activityTypeId` | number | `6` | Garmin activity type ID |
| `title` | string | `"Black Mountain"` | Activity name |
| `date` | string | `"2026-01-10"` | ISO date (YYYY-MM-DD) |
| `duration` | number | `3001382` | Total duration in **milliseconds** |
| `distance` | number | `805000` | Total distance in **centimeters** (divide by 100 for meters) |
| `calories` | number | `1881` | Total kcal |
| `averageHR` | number | `122` | Average heart rate, BPM |
| `startTimestampLocal` | string | `"2025-12-25T09:27:02.0"` | ISO local datetime |
| `elapsedDuration` | number | `3001.382` | Elapsed duration in **seconds** (= `duration / 1000`) |
| `lapCount` | number | `9` | Number of laps |
| `isParent` | boolean | `false` | Multi-sport parent flag |
| `hasSplits` | boolean | `true` | Whether split data exists |
| `autoCalcCalories` | boolean | `false` | |
| `decoDive` | boolean | `false` | |

**Important unit differences from APIs 1 & 2:**
- `duration` here is in **milliseconds** (APIs 1 & 2 use seconds)
- `distance` here is in **centimeters** (APIs 1 & 2 use meters)

#### Conditionally-Present Fields (null for some activity types)

| Field | Type | Example | Populated For | Notes |
|-------|------|---------|---------------|-------|
| `maxSpeed` | number | `3.667` | Most activities (145/167) | In **m/s** |
| `totalAscent` | number | `1585.54` | Running/hiking (103/167) | In **meters** |
| `noOfSplits` | number | `8` | Running/hiking (106/167) | Number of run/walk/stand splits |
| `climbDuration` | number | `3001.38` | Running/hiking (106/167) | In **seconds** |
| `activeSplitSummaryDuration` | number | `3001.38` | Running/hiking (106/167) | Active split total, **seconds** |
| `activeSplitSummaryDistance` | number | `8112.21` | Running/hiking (106/167) | Active split total, **meters** |
| `maxSplitDistance` | number | `8112` | Running/hiking (106/167) | Longest split, **meters** (integer) |
| `maxSplitSpeed` | number | `3.667` | Running/hiking (105/167) | In **m/s** |
| `activeSets` | number | `19` | Strength/pilates (21/167) | Number of exercise sets |
| `avgRespirationRate` | number | `29.66` | Sparse (14/167) | Breaths per minute |

#### Known `activityTypeId` Values (from 3-month sample)

| `activityTypeId` | Activity | Count |
|-------------------|----------|-------|
| `1` | Running (road) | 59 |
| `8` | Track Running | 27 |
| `13` | Strength Training | 21 |
| `225` | Pickleball | 21 |
| `6` | Trail Running | 17 |
| `3` | Hiking | 11 |
| `2` | Cycling | 4 |
| `9` | Walking | 3 |
| `18` | Treadmill Running | 2 |
| `25` | Indoor Cycling | 1 |
| `31` | Stair Stepper | 1 |

---

### Item Type: `goal`

Training goals appear as **two entries**: one with `isStart: true` on the start date and one with `isStart: false` on the end date.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `40548782` | Goal ID |
| `itemType` | string | `"goal"` | |
| `title` | string | `"Run 3000 km in 2026"` | Goal description |
| `date` | string | `"2026-01-01"` | Start or end date |
| `isStart` | boolean | `true` | `true` = goal start, `false` = goal end |

---

### Item Type: `weight`

Body weight measurements from Garmin's scale or manual entry.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `1770396195168` | Measurement ID |
| `itemType` | string | `"weight"` | |
| `date` | string | `"2026-02-06"` | ISO date |
| `weight` | number | `72400` | Body weight in **grams** (divide by 1000 for kg) |
| `difference` | number | `-99` | Change from previous measurement in **grams** |

---

### Item Type: `nap`

Detected nap sessions from the wearable device.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `itemType` | string | `"nap"` | |
| `date` | string | `"2026-02-04"` | ISO date |
| `duration` | number | `3060` | Nap duration in **seconds** (note: unlike activity `duration` which is milliseconds) |
| `napStartTimeLocal` | string | `"2026-02-04T14:16:15"` | ISO local datetime |

Note: `id` is `null` for naps.

---

### Item Type: `note`

User-created text notes attached to a date.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `126088664` | Note ID |
| `itemType` | string | `"note"` | |
| `title` | string | `"Ankle issue"` | Note text (may contain Chinese characters) |
| `date` | string | `"2025-12-30"` | ISO date |

---

### Item Type: `event`

Scheduled races or events (e.g., from Garmin's event calendar).

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `itemType` | string | `"event"` | |
| `activityTypeId` | number | `6` | Expected activity type |
| `title` | string | `"Marin Ultra Challenge (50K)"` | Event name |
| `date` | string | `"2026-03-14"` | ISO date |
| `url` | string | `"https://www.ahotu.com/..."` | External event URL |
| `isRace` | boolean | `true` | Whether it's a race |
| `location` | string | `"Sausalito, California, US"` | Event location |
| `eventTimeLocal` | object | See below | Local start time |
| `completionTarget` | object | See below | Target distance/time |
| `shareableEventUuid` | string | `"1d964b26-..."` | UUID for sharing |
| `subscribed` | boolean | `true` | Whether user subscribed to the event |
| `shareableEvent` | boolean | `true` | |
| `primaryEvent` | boolean | `false` | |

Note: `id` is `null` for events.

#### `eventTimeLocal` Object

```json
{ "startTimeHhMm": "07:00", "timeZoneId": "America/Los_Angeles" }
```

#### `completionTarget` Object

```json
{ "value": 50000, "unit": "meter", "unitType": "distance" }
```

---

### Unit Summary (Calendar API)

| Measurement | Unit | Notes |
|-------------|------|-------|
| Activity duration | milliseconds | Different from APIs 1–6 (which use seconds) |
| Activity distance | centimeters | Different from APIs 1–6 (which use meters) |
| Nap duration | seconds | Inconsistent with activity duration |
| Elapsed duration | seconds | = activity duration / 1000 |
| Split distances | meters | `activeSplitSummaryDistance`, `maxSplitDistance` |
| Speed | m/s | Same as APIs 1–6 |
| Elevation | meters | `totalAscent` |
| Weight | grams | Divide by 1000 for kg |
| Weight difference | grams | |
| Calories | kcal | |
| Heart rate | BPM | |
| Respiration | breaths/min | |
| Event distance target | meters | In `completionTarget.value` |

---

### Data Characteristics (from 3-month sample: Jan–Mar 2026)

- **Total items**: 216 across January (104), February (87), March (25)
- **167 activities** spanning 11 distinct activity types — dominated by running (59), track running (27), strength (21), and pickleball (21)
- **Calendar includes padding days** from adjacent months (e.g., January response includes items from late December 2025)
- **Goals have paired start/end entries** — each goal appears twice (once at start date, once at end)
- **Weight** values show entries roughly every 3–7 days, weight range ~71.5–74.0 kg
- **Notes** may contain Chinese text
- **Nap entries may be duplicated** across month boundaries (same nap appears in both months' responses when near month edge)

### Relationship to Other APIs

| Aspect | Calendar API (API 7) | Activity List (API 1) |
|--------|---------------------|----------------------|
| Service | `calendar-service` | `activitylist-service` |
| Scope | All item types (activities, goals, weight, naps, notes, events) | Activities only |
| Granularity | Monthly | Paginated with filters |
| Activity detail | Summary only (distance, duration, calories, HR, speed) | Full per-activity data (HR zones, power, running dynamics, splits, GPS, etc.) |
| Duration unit | Milliseconds | Seconds |
| Distance unit | Centimeters | Meters |
| `activityId` | `id` field | `activityId` field (same value) |

- Uses same `activityTypeId` values as other APIs, but reveals more types (pickleball `225`, track running `8`, stair stepper `31`, etc.) not seen in the API 1 sample
- The `id` for activities maps to `activityId` in APIs 1 & 2, enabling drill-down to full activity detail
- Weight data is unique to this API — not available from activity or metrics services
- Goal tracking (with start/end markers) is unique to this API
- Nap data overlaps with API 6 (`dailyNapDTOS`) but with less detail (no feedback, no UTC offset)
- Note `title` in the calendar is the short name; full note content requires API 8 (Note Detail)

---
---

## API 8: Calendar Note Detail

```bash
curl 'https://connect.garmin.com/gc-api/calendar-service/note/{noteId}' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Same `calendar-service` as API 7 (Monthly Calendar), but a sub-endpoint for retrieving a single note's full content. The calendar API (API 7) only returns the note's `title`; this endpoint provides the full `content` body text.

### Path Parameters

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `{noteId}` | number | `126088664` | Note ID from the calendar item's `id` field (API 7) |

### File Format

- **Compression**: Brotli (same as APIs 1–7)
- **Underlying format**: JSON **object**

### Response Structure

```json
{
  "id": 126088664,
  "noteName": "Ankle issue",
  "content": "The left ankle is not feeling good, and it also (likely) resulted in the knee pain after yesterday run\n\nThe ankle issue started from a hiking in Utah in end of November. It has been lasting for more than one month already.",
  "date": "2025-12-30"
}
```

### Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | number | `126088664` | Same as the note `id` in API 7's calendar items |
| `noteName` | string | `"Ankle issue"` | Same as `title` in API 7's calendar item |
| `content` | string | `"The left ankle is..."` | Full note body text. May be multi-line (`\n` separators). May contain Chinese characters. |
| `date` | string | `"2025-12-30"` | ISO date (YYYY-MM-DD), same as API 7 |

### Relationship to API 7

| Aspect | API 7 (Calendar) | API 8 (Note Detail) |
|--------|------------------|---------------------|
| Endpoint | `calendar-service/year/{y}/month/{m}` | `calendar-service/note/{noteId}` |
| Note info | `title` only (short name) | `noteName` + full `content` body |
| Field name | `title` | `noteName` (same value) |
| Use case | List/discover notes | Read full note text |

- The `id` from a calendar note item (API 7) is used directly as the `{noteId}` path parameter
- This is the only way to retrieve the full note body — the calendar endpoint only surfaces the title

---

## API 9: Activity File Download (FIT Export)

```bash
curl 'https://connect.garmin.com/gc-api/download-service/files/activity/{activityId}' \
-X 'GET' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Cookie: <cookie>' \
-H 'Sec-Fetch-Mode: cors' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Accept-Encoding: gzip, deflate, br, zstd' \
-H 'Sec-Fetch-Dest: empty' \
-H 'Connect-Csrf-Token: <csrf-token>' \
-H 'Priority: u=3, i'
```

### Overview

Downloads the original activity file (FIT format) as a ZIP archive. This is the raw data recorded by the Garmin device, containing detailed time-series data (GPS trackpoints, heart rate samples, cadence, power, etc.) that is not available through the JSON activity APIs (APIs 1 & 2).

### Path Parameters

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `{activityId}` | number | `22048373565` | Activity ID from the activity list (API 1) or activity detail (API 2) |

### Response Format

- **Content-Type**: `application/x-zip-compressed`
- **Content-Disposition**: `attachment; filename="{activityId}.zip"` (e.g. `22048373565.zip`)
- **Compression**: Not Brotli — the response is a raw ZIP archive (unlike APIs 1–8 which return Brotli-compressed JSON)
- **Cache-Control**: `no-cache, no-store, private`

### ZIP Contents

The ZIP archive contains a single file:

| File | Format | Example |
|------|--------|---------|
| `{activityId}_ACTIVITY.fit` | Garmin FIT (Flexible and Interoperable Data Transfer) | `22048373565_ACTIVITY.fit` |

Example from a real download:
- **ZIP size**: 47,842 bytes
- **FIT file size** (uncompressed): 116,612 bytes

### How to Extract

#### CLI

```bash
# Download and extract
curl -o activity.zip 'https://connect.garmin.com/gc-api/download-service/files/activity/{activityId}' \
  -H 'Cookie: <cookie>' -H 'Connect-Csrf-Token: <csrf-token>'
unzip activity.zip
# Result: {activityId}_ACTIVITY.fit
```

#### Python

```python
import zipfile, io

# Assuming `response_content` is the raw bytes from the API
with zipfile.ZipFile(io.BytesIO(response_content)) as zf:
    zf.extractall('.')  # Extracts {activityId}_ACTIVITY.fit
```

### FIT File Format

The FIT (Flexible and Interoperable Data Transfer) protocol is Garmin's binary format for activity data. It contains far more granular data than the JSON APIs, including:

- **GPS trackpoints** — latitude, longitude, altitude at each recording interval
- **Sensor time-series** — heart rate, cadence, power, speed at each second/interval
- **Lap/split details** — auto-lap and manual lap markers with per-lap summaries
- **Device info** — hardware model, firmware version, sensor accessories
- **Running dynamics** — ground contact time, vertical oscillation, etc.
- **Developer fields** — third-party app data (e.g. Stryd, Running Power)

To parse FIT files in Python, use the `fitdecode` or `fitparse` libraries:

```python
# pip install fitdecode
import fitdecode

with fitdecode.FitReader('{activityId}_ACTIVITY.fit') as fit:
    for frame in fit:
        if isinstance(frame, fitdecode.FitDataMessage):
            if frame.name == 'record':  # Per-second data points
                print(frame.get_value('heart_rate'), frame.get_value('position_lat'))
```

### Relationship to Other APIs

| Aspect | APIs 1 & 2 (Activity JSON) | API 9 (File Download) |
|--------|---------------------------|----------------------|
| Format | JSON (summary/aggregate data) | Binary FIT (raw device recording) |
| Data granularity | Per-activity summaries, split summaries | Per-second time-series, GPS trackpoints |
| GPS data | Start/end lat/lng only | Full GPS track |
| Heart rate | Min/max/avg only | Every sample point |
| Use case | Dashboards, search, analytics | Route mapping, detailed analysis, re-import |
| Response type | Brotli-compressed JSON | ZIP-compressed FIT file |
