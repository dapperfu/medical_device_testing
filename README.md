# medical_device_testing

Mock vital-signs patient monitor and pytest harness.

This tree is a training mock. The user confirmed software safety class C for the exercise on 2026-10-20. The documents follow that activity list. They are not a conformity, certification, or regulatory submission.

## Run

```bash
make build
make test
make run
make lint
make strictdoc-generate
```

`make test` writes `docs/pytest-report.html`. Requirement HTML is under `docs/html/`. `docs/index.html` links both for GitHub Pages when the site source is the `docs/` folder on `main`.
