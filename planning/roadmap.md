# Roadmap

Index of every spec. `Status` and `Stage` are written only by `trace status --write`
(and by `trace start`/`done`); everything else by people and skills. Format:
`skills/spectrace-start/assets/format.md`.

| ID  | Spec              | Status | Depends on    | Stage | Priority |
|-----|-------------------|--------|---------------|-------|----------|
| 001 | format-and-trace  | done        | —             | —     | 1        |
| 002 | start             | done        | 001           | —      | 2        |
| 003 | plan              | done        | 001, 002      | —      | 3        |
| 004 | change            | done        | 001, 003      | —      | 4        |
| 005 | distribution      | done        | 002, 003, 004 | —      | 5        |
| 006 | e2e-verification  | done        | 005           | —      | 6        |
