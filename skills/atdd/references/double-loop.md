# Double-Loop TDD

## 二重ループの構造

```text
Outer Loop (ATDD)
  Acceptance Test を書く ──────────────► RED
        │
        │   Inner Loop (TDD)
        │     Unit Test を書く ────────► RED
        │     部品を実装する ──────────► GREEN
        │     リファクタリングする
        │     （必要な部品の数だけ繰り返す）
        ▼
  Acceptance Test が通る ──────────────► GREEN
        │
        ▼
  次の Acceptance Test へ
```

外側が「何ができれば完成か」を、内側が「どう作るか」を担当する。

## ACとATの対応

定石は 1 AC = 1 AT だが、ACの粒度によってはATが膨大になり、AIに書かせてもCIで回しても費用が見合わなくなる。

本Skillは 1 User Story = 1 AT を既定とする。複数のACは同一AT内の検証で網羅し、
どのACが壊れたのかは検証名で区別する。ATの本数を抑える代わりに、失敗箇所の特定を検証名の設計へ移している。

ユーザーに観測可能な振る舞いを持たないUser Story（ツールチェーン整備、設定変更など）はATの対象にしない。

## 内側の自由度

重要なのは外側をATDD化することであり、内側の手法は選択してよい。TDD、SDD、BDDのいずれでも、
ATが実装から隔離されている限り、外側の保証は変わらない。

## 上流工程との関係

ATが浅くなる原因は、ほとんどの場合ATDDの手順ではなくその前段にある。

```text
要件定義が不十分  →  ACの質が低い  →  ATが浅い  →  「テストが通った」が無意味になる
```

したがって、ATを書き直す前にACを、ACを書き直す前に要件を疑う。
これはAI固有の話ではなく、人間が開発するときに重視してきたものを、AIに作らせるときにも同じく重視するということである。

上流（要件、User Story、AC）は人間の関与を強く保ち、下流（実装、Unit Test、リファクタリング）をAIへ委譲する。

## 出典

- 大園博昭「なぜ『テストが通った』はAI時代に信用できなくなったのか 〜受け入れテスト駆動開発(ATDD)にたどり着くまで〜」
  Developers Summit 2026 FUKUOKA, 2026-09-11. <https://speakerdeck.com/o3/2026-devsumi-ozono>
- Elisabeth Hendrickson, "Acceptance Test Driven Development (ATDD) Revisited", Curious Duck, 2024-06-27.
- Ken Pugh, "Lean-Agile Acceptance Test-Driven Development: Better Software Through Collaboration", Addison-Wesley, 2011.
