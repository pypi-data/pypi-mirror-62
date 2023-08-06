# pyPhase Project-builder

This Generator will create a ready-to-go pyPhase-Project, based on a config-Yaml. 

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

run with `python myProject`

### complete
```YAML
name: "sleepClassificationCNN"
namespace: tud.ibmt
exporter:
    - ObjectExporter
    - KerasExporter
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


### Development

The generator will create stubs for each phase, publisher, storage, exporter and generator that 
does not exists in the pyPhase-Package. The stubs are in the project folder and implement empty
method that are required.

To implement your project, you only need to fill those methods. For the minimal example you need
to fill the `main`-methods of Phase1 (`myProject/phases/Phase1.py`) and Phase2.