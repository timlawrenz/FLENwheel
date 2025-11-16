graph TD
    subgraph "Flywheel 1: FLUX Character LoRA"
        direction TB
        A(1. Source Material<br/>[Photos, Sketches]) --> B{2. Qwen-VL + <i>Qwen LoRA (v1)</i>};
        B --> C[3. Enriched Dataset<br/>(Varied Backgrounds, Lighting)];
        C --> D(4. Train on 4090);
        D --> E(5. FLUX + <i>Char LoRA (v1)</i>);
        E --> F[6. Synthetic Data<br/>(New Poses, Scenes)];
        F --> G{7. Human Review<br/>(Guided Curation)};
        G -- "Good" --> H[8. Pristine Dataset<br/>(For next FLUX LoRA)];
        H --> D;
    end

    subgraph "Flywheel 2: Qwen-VL Editor LoRA"
        direction TB
        G -- "Good & Corrected" --> I[9. Qwen Dataset<br/>(source, text, result)];
        I --> J(10. Train on 4090<br/>[PEFT/QLoRA]);
        J --> K[11. <i>Qwen LoRA (v2)</i>];
    end

    %% --- Connections ---
    K -.-> B;

    %% --- Styling ---
    classDef main fill:#e6f3ff,stroke:#b3d9ff,stroke-width:2px;
    class A,C,F,H main;

    classDef process fill:#fff,stroke:#ccc,stroke-width:2px;
    class B,G process;

    classDef train fill:#ffe6e6,stroke:#ffb3b3,stroke-width:2px;
    class D,J train;

    classDef model fill:#d4fadd,stroke:#90c695,stroke-width:2px,font-weight:bold;
    class E,K model;

    classDef dataset fill:#fff2cc,stroke:#ffd966,stroke-width:2px;
    class I dataset;

    linkStyle 0 stroke:#007bff,stroke-width:1.5px;
    linkStyle 1 stroke:#007bff,stroke-width:1.5px;
    linkStyle 2 stroke:#007bff,stroke-width:1.5px;
    linkStyle 3 stroke:#007bff,stroke-width:1.5px;
    linkStyle 4 stroke:#007bff,stroke-width:1.5px;
    linkStyle 5 stroke:#28a745,stroke-width:1.5px,stroke-dasharray: 5 5;
    linkStyle 6 stroke:#007bff,stroke-width:1.5px;
    linkStyle 7 stroke:#dc3545,stroke-width:1.5px,stroke-dasharray: 5 5;
    linkStyle 8 stroke:#dc3545,stroke-width:1.5px;
    linkStyle 9 stroke:#dc3545,stroke-width:1.5px;
    linkStyle 10 stroke:#007bff,stroke-width:2.5px,stroke-dasharray: 8 3;
