# Garmin Connect API Endpoints (from garth package)

Supplementary API reference extracted from the [garth](https://github.com/matin/garth) Python package (v0.6.3). Use these endpoints as a fallback when the primary `garmin-api-spec.md` does not cover the data you need.

All endpoints are under `https://connectapi.garmin.com` and require OAuth2 Bearer auth.

---

## Already covered in garmin-api-spec.md

These endpoints overlap with the primary spec and are listed here only for cross-reference:

| Endpoint | garmin-api-spec.md API # |
|---|---|
| `/activitylist-service/activities/search/activities` | API 1 |
| `/activity-service/activity/{id}` | API 2 |
| `/metrics-service/metrics/hillscore` | API 3 |
| `/metrics-service/metrics/endurancescore` | API 4 |
| `/wellness-service/stats/daily/sleep/score/{start}/{end}` | API 5 |
| `/sleep-service/sleep/dailySleepData?date={date}` | API 6 |

---

## Additional endpoints NOT in garmin-api-spec.md

### Daily Summary (steps, calories, HR, stress, body battery, SpO2, floors)

```
GET /usersummary-service/usersummary/daily/?calendarDate={YYYY-MM-DD}
```

Returns a single object with:

| Field | Type | Description |
|---|---|---|
| `userProfileId` | int | User ID |
| `calendarDate` | date | Date |
| `totalKilocalories` | int | Total calories (BMR + active) |
| `activeKilocalories` | int | Active calories only |
| `totalSteps` | int | Total steps |
| `totalDistanceMeters` | int | Total distance in meters |
| `minHeartRate` | int | Min HR for the day |
| `maxHeartRate` | int | Max HR for the day |
| `restingHeartRate` | int | Resting HR |
| `lastSevenDaysAvgRestingHeartRate` | int | 7-day avg resting HR |
| `maxStressLevel` | int | Max stress (0-100) |
| `averageStressLevel` | int | Avg stress (0-100) |
| `stressQualifier` | string | e.g. "low", "medium" |
| `bodyBatteryAtWakeTime` | int | Body battery at wake |
| `bodyBatteryHighestValue` | int | Peak body battery |
| `bodyBatteryLowestValue` | int | Lowest body battery |
| `moderateIntensityMinutes` | int | Moderate intensity mins |
| `vigorousIntensityMinutes` | int | Vigorous intensity mins |
| `activeSeconds` | int | Active time |
| `highlyActiveSeconds` | int | High-activity time |
| `sedentarySeconds` | int | Sedentary time |
| `sleepingSeconds` | int | Sleep time |
| `floorsAscended` | float | Floors climbed |
| `floorsDescended` | float | Floors descended |
| `averageSpo2` | int | Avg SpO2 |
| `lowestSpo2` | int | Lowest SpO2 |
| `avgWakingRespirationValue` | int | Avg respiration |
| `highestRespirationValue` | int | Max respiration |
| `lowestRespirationValue` | int | Min respiration |

---

### Daily Heart Rate (full time-series)

```
GET /wellness-service/wellness/dailyHeartRate/?date={YYYY-MM-DD}
```

Returns a single object with:

| Field | Type | Description |
|---|---|---|
| `userProfilePK` | int | User ID |
| `calendarDate` | date | Date |
| `startTimestampGMT` / `startTimestampLocal` | datetime | Day start |
| `endTimestampGMT` / `endTimestampLocal` | datetime | Day end |
| `maxHeartRate` | int | Max HR |
| `minHeartRate` | int | Min HR |
| `restingHeartRate` | int | Resting HR |
| `lastSevenDaysAvgRestingHeartRate` | int | 7-day avg resting HR |
| `heartRateValues` | array | Time-series: `[[timestamp_ms, hr_value], ...]` (null hr = no reading) |

---

### HRV Detail (nightly readings + baseline)

```
GET /hrv-service/hrv/{YYYY-MM-DD}
```

Returns a single object with:

| Field | Type | Description |
|---|---|---|
| `userProfilePK` | int | User ID |
| `hrvSummary.calendarDate` | date | Date |
| `hrvSummary.weeklyAvg` | int | 7-day HRV average |
| `hrvSummary.lastNightAvg` | int | Last night's avg HRV |
| `hrvSummary.lastNight5MinHigh` | int | Best 5-min HRV window |
| `hrvSummary.status` | string | e.g. "BALANCED" |
| `hrvSummary.feedbackPhrase` | string | Garmin's text feedback |
| `hrvSummary.baseline.lowUpper` | int | Baseline low boundary |
| `hrvSummary.baseline.balancedLow` | int | Balanced range low |
| `hrvSummary.baseline.balancedUpper` | int | Balanced range high |
| `hrvReadings` | array | `[{hrvValue, readingTimeGMT, readingTimeLocal}, ...]` |
| `sleepStartTimestampGMT` / `sleepEndTimestampGMT` | datetime | Sleep window |

---

### HRV Daily Aggregates

```
GET /hrv-service/hrv/daily/{startDate}/{endDate}
```

Response: `{ "hrvSummaries": [...] }` — array of daily HRV summaries (same fields as `hrvSummary` above). Max 28 days per request.

---

### Stress Daily Aggregates

```
GET /usersummary-service/stats/stress/daily/{startDate}/{endDate}
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `overallStressLevel` | int | Overall stress (0-100) |
| `restStressDuration` | int | Seconds at rest stress |
| `lowStressDuration` | int | Seconds at low stress |
| `mediumStressDuration` | int | Seconds at medium stress |
| `highStressDuration` | int | Seconds at high stress |

Max 28 days per request.

---

### Stress Weekly Aggregates

```
GET /usersummary-service/stats/stress/weekly/{endDate}/{numWeeks}
```

Returns an array. Each entry: `{ calendarDate, value }` (weekly avg stress). Max 52 weeks per request.

---

### Body Battery & Stress Time-Series (combined)

```
GET /wellness-service/wellness/dailyStress/{YYYY-MM-DD}
```

Returns a single object with:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `maxStressLevel` | int | Max stress |
| `avgStressLevel` | int | Avg stress |
| `stressChartValueOffset` | int | Chart rendering offset |
| `stressValuesArray` | array | `[[timestamp_ms, stress_level], ...]` |
| `bodyBatteryValuesArray` | array | `[[timestamp_ms, status, level, version], ...]` |

---

### Body Battery Events (sleep/activity impacts)

```
GET /wellness-service/wellness/bodyBattery/events/{YYYY-MM-DD}
```

Returns an array of events. Each event:

| Field | Type | Description |
|---|---|---|
| `event.eventType` | string | e.g. sleep, activity |
| `event.eventStartTimeGmt` | datetime | Event start |
| `event.timezoneOffset` | int | TZ offset in ms |
| `event.durationInMilliseconds` | int | Event duration |
| `event.bodyBatteryImpact` | int | Impact on body battery |
| `event.feedbackType` | string | Feedback category |
| `event.shortFeedback` | string | Text description |
| `activityName` | string | Activity name (if activity event) |
| `activityType` | string | Activity type key |
| `activityId` | int/string | Activity ID |
| `averageStress` | float | Avg stress during event |
| `stressValuesArray` | array | Stress time-series for event |
| `bodyBatteryValuesArray` | array | Body battery time-series for event |

---

### Steps Daily Aggregates

```
GET /usersummary-service/stats/steps/daily/{startDate}/{endDate}
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `totalSteps` | int | Total steps |
| `totalDistance` | int | Distance (meters) |
| `stepGoal` | int | Daily step goal |

Max 28 days per request.

---

### Steps Weekly Aggregates

```
GET /usersummary-service/stats/steps/weekly/{endDate}/{numWeeks}
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Week start date |
| `totalSteps` | int | Total weekly steps |
| `averageSteps` | float | Daily avg steps |
| `totalDistance` | float | Total distance |
| `averageDistance` | float | Daily avg distance |
| `wellnessDataDaysCount` | int | Days with data |

Max 52 weeks per request.

---

### Weight (single day)

```
GET /weight-service/weight/dayview/{YYYY-MM-DD}
```

Response: `{ "dateWeightList": [...] }` — array of weight entries for that day. Each entry:

| Field | Type | Description |
|---|---|---|
| `samplePk` | int | Entry ID |
| `calendarDate` | date | Date |
| `weight` | int | Weight in grams |
| `bmi` | float | BMI |
| `bodyFat` | float | Body fat % |
| `bodyWater` | float | Body water % |
| `boneMass` | int | Bone mass (grams) |
| `muscleMass` | int | Muscle mass (grams) |
| `physiqueRating` | float | Physique rating |
| `visceralFat` | float | Visceral fat |
| `metabolicAge` | int | Metabolic age |
| `sourceType` | string | e.g. "INDEX_SCALE" |
| `timestampGMT` | int | Timestamp (ms) |
| `date` | int | Local timestamp (ms) |
| `weightDelta` | float | Change from previous |

---

### Weight (date range)

```
GET /weight-service/weight/range/{startDate}/{endDate}?includeAll=true
```

Response: `{ "dailyWeightSummaries": [ { "allWeightMetrics": [...] }, ... ] }` — same fields as above per entry.

---

### Intensity Minutes (daily)

```
GET /usersummary-service/stats/im/daily/{startDate}/{endDate}
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `weeklyGoal` | int | Weekly goal (minutes) |
| `moderateValue` | int | Moderate minutes |
| `vigorousValue` | int | Vigorous minutes |

Max 28 days per request.

---

### Intensity Minutes (weekly)

```
GET /usersummary-service/stats/im/weekly/{startDate}/{endDate}
```

Same fields as daily, aggregated weekly. Max 52 weeks per request.

---

### Hydration (daily aggregates)

```
GET /usersummary-service/stats/hydration/daily/{startDate}/{endDate}
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `valueInML` | float | Water intake (mL) |
| `goalInML` | float | Daily goal (mL) |

Max 28 days per request.

---

### Hydration (log intake) — WRITE endpoint

```
PUT /usersummary-service/usersummary/hydration/log
Content-Type: application/json

{
  "valueInML": "500",
  "timestampLocal": "2026-03-02T12:00:00.0",
  "userProfileId": "<profile_id>"
}
```

Returns: `{ userId, calendarDate, valueInML, goalInML, sweatLossInML, ... }`

---

### Training Readiness (all contexts for a day)

```
GET /metrics-service/metrics/trainingreadiness/{YYYY-MM-DD}
```

Returns an array (multiple contexts, e.g. AFTER_WAKEUP_RESET, CURRENT). Each entry:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `score` | int | Readiness score (0-100) |
| `level` | string | e.g. "PRIME", "HIGH" |
| `feedbackShort` / `feedbackLong` | string | Garmin text |
| `sleepScore` | int | Sleep score component |
| `sleepScoreFactorPercent` | int | Sleep contribution % |
| `recoveryTime` | float | Recovery time (hours) |
| `recoveryTimeFactorPercent` | int | Recovery time contribution % |
| `acuteLoad` | int | Acute training load |
| `acwrFactorPercent` | int | ACWR contribution % |
| `hrvWeeklyAverage` | int | HRV weekly avg |
| `hrvFactorPercent` | int | HRV contribution % |
| `stressHistoryFactorPercent` | int | Stress contribution % |
| `sleepHistoryFactorPercent` | int | Sleep history contribution % |
| `inputContext` | string | `"AFTER_WAKEUP_RESET"` or `"CURRENT"` |
| `validSleep` | bool | Whether sleep data was valid |
| `deviceId` | int | Device ID |

To get only morning readiness, filter for `inputContext == "AFTER_WAKEUP_RESET"`.

---

### Training Status (daily/latest)

```
GET /mobile-gateway/usersummary/trainingstatus/latest/{YYYY-MM-DD}
```

Response is nested: `mostRecentTrainingStatus.payload.latestTrainingStatusData.{deviceId}.{...}`. Key fields:

| Field | Type | Description |
|---|---|---|
| `calendarDate` | date | Date |
| `weeklyTrainingLoad` | int | Weekly load |
| `trainingStatus` | int | Status code |
| `trainingStatusFeedbackPhrase` | string | e.g. "Productive" |
| `loadTunnelMin` / `loadTunnelMax` | int | Optimal load range |
| `loadLevelTrend` | string/int | Load trend |
| `fitnessTrend` | int | VO2 max trend |
| `acwrPercent` | int | Acute:chronic ratio % |
| `acwrStatus` | string | e.g. "OPTIMAL" |
| `dailyTrainingLoadAcute` | int | Today's acute load |
| `dailyTrainingLoadChronic` | int | Chronic load |
| `dailyAcuteChronicWorkloadRatio` | float | ACWR ratio |
| `maxTrainingLoadChronic` / `minTrainingLoadChronic` | float | Chronic range |

Max 28 days per request.

---

### Training Status (weekly)

```
GET /mobile-gateway/usersummary/trainingstatus/weekly/{startDate}/{endDate}
```

Response nested under `weeklyTrainingStatus.payload.reportData.{deviceId}.[...]`. Same fields as daily. Max 52 weeks per request.

---

### Training Status (monthly)

```
GET /mobile-gateway/usersummary/trainingstatus/monthly/{startDate}/{endDate}
```

Response nested under `monthlyTrainingStatus.payload.reportData.{deviceId}.[...]`. Same fields. Max 12 months per request.

---

### Fitness Stats (activities with coaching data)

```
GET /fitnessstats-service/activity/all?startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}&standardizedUnits=true&metric=activityType&metric=workoutType&metric=aerobicTrainingEffect&metric=adaptiveCoachingWorkoutStatus&metric=parentId&metric=workoutGroupEnumerator
```

Returns an array. Each entry:

| Field | Type | Description |
|---|---|---|
| `activityId` | int | Activity ID |
| `startLocal` | datetime | Local start time |
| `activityType` | string | Activity type key |
| `workoutGroupEnumerator` | int | Workout group |
| `aerobicTrainingEffect` | float | Aerobic TE (0-5) |
| `workoutType` | string | Workout type label |
| `adaptiveCoachingWorkoutStatus` | string | e.g. "COMPLETED_VIA_ACTIVITY" |
| `parentId` | int | Parent activity (for multisport) |

---

### Sleep Detail (alternative endpoint with movement data)

```
GET /wellness-service/wellness/dailySleepData/{username}?nonSleepBufferMinutes=60&date={YYYY-MM-DD}
```

Similar to the `/sleep-service/sleep/dailySleepData` endpoint (API 6 in main spec) but includes `sleepMovement` array: `[{ startGMT, endGMT, activityLevel }, ...]`.

---

### Activity Update — WRITE endpoint

```
PUT /activity-service/activity/{activityId}
Content-Type: application/json

{
  "activityId": 12345678901,
  "activityName": "New Name",
  "description": "New description"
}
```

Updates the activity name and/or description.

---

### User Profile

```
GET /userprofile-service/socialProfile
```

Returns user profile data:

| Field | Type | Description |
|---|---|---|
| `displayName` | string | Display name |
| `fullName` | string | Full name |
| `userName` | string | Username |
| `profileImageUrlLarge/Medium/Small` | string | Avatar URLs |
| `location` | string | Location |
| `bio` | string | Bio text |
| `primaryActivity` | string | Primary activity type |
| `favoriteActivityTypes` | array | Preferred activities |
| `runningTrainingSpeed` | float | Running speed setting |
| `cyclingTrainingSpeed` | float | Cycling speed setting |
| `profileVisibility` | string | Privacy setting |
| `userLevel` | int | Gamification level |
| `userPoint` | int | Points |
| `userPro` | bool | Pro subscription |

---

### User Settings

```
GET /userprofile-service/userprofile/user-settings
```

Returns user settings:

| Field | Type | Description |
|---|---|---|
| `userData.gender` | string | Gender |
| `userData.weight` | float | Weight |
| `userData.height` | float | Height |
| `userData.birthDate` | date | Birth date |
| `userData.measurementSystem` | string | Metric/imperial |
| `userData.timeFormat` | string | 12h/24h |
| `userData.vo2MaxRunning` | float | VO2 max (running) |
| `userData.vo2MaxCycling` | float | VO2 max (cycling) |
| `userData.lactateThresholdSpeed` | float | LT speed |
| `userData.lactateThresholdHeartRate` | float | LT heart rate |
| `userData.hydrationMeasurementUnit` | string | mL / oz |
| `userData.hydrationAutoGoalEnabled` | bool | Auto hydration goal |
| `userSleep.sleepTime` | int | Bedtime (seconds from midnight) |
| `userSleep.wakeTime` | int | Wake time (seconds from midnight) |
| `userSleepWindows` | array | `[{ sleepWindowFrequency, startSleepTimeSecondsFromMidnight, endSleepTimeSecondsFromMidnight }]` |

---

### Upload Activity File — WRITE endpoint

```
POST /upload-service/upload
Content-Type: multipart/form-data

file: <FIT/GPX/TCX file>
```

Uploads an activity file (FIT, GPX, or TCX format).

---

## Pagination Notes

- **Stats endpoints** (steps, stress, hydration, intensity minutes, HRV daily) have per-request page size limits (typically 28 days or 52 weeks). For longer ranges, issue multiple requests with offset date windows.
- **Activity list** uses `limit` + `start` offset pagination.

## Base URL Note

garth uses `connectapi.garmin.com` as the base URL (OAuth2 auth). Our CLI uses `connect.garmin.com/gc-api` for cookie auth. The API paths are the same — only the host differs based on auth method.
