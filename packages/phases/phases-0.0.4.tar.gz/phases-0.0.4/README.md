# Phases Boilerplate

## Setup

`pip install phases`

## create `project.yaml`

### minimal
```YAML
name: "myProject"
namespace: myGroup
phases:
    stage1:
        - name: Phase1
          description: my first phase
        - name: Phase2
          description: my second phase
```

### complete
```YAML
name: "sleepClassificationCNN"
namespace: tud.ibmt
classes:
    - Wach
    - Leichter Schlaf
    - Tiefer Schlaf
    - REM
publisher:
    - DotSience
phases:
    prepareData:
        - name: DataWrapper
          description: get EDF Data
          exports: 
            - trainingRaw
            - validationRaw
            - evaluationRaw
        - name: EDF4SleepStages
          description: Prepare EDF Data for sleep stage recognition
          exports: 
            - trainingTransformed
            - validationTransformed
    train:
        - name: SleepPhaseDetectionModel
          description: Create Model for sleep stage recognition
          exports: 
            - model
    evaluate:
        - name: SleepPhaseDetectionModel
          description: Create Model for sleep stage recognition
```

### Generate

`phases create`