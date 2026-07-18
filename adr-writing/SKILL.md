---
name: adr-writing
description: リファクタリングや設計変更後のADRを作成する際に使用する。関連するコード、Pull Request、Issue、既存ADRを確認し、WhatとWhyを中心とした設計上の意思決定を記録する。
---

# ADR Writing

## 目的

設計上の意思決定を Architecture Decision Record (ADR) として記録する。

コードだけでは分からない設計判断（Why）と、最終的に採用された設計（What）を残し、将来の人間およびAIが同じ判断を再現できるようにする。

ADRは作業記録や設計書ではなく、意思決定を記録する文書として扱う。

## 手順

1. このSkill全文を読み、読了を最初の応答で明示する。
2. ADRを作成すべき変更か確認する。
3. 関連するコード、Pull Request、Issue、既存ADRを確認する。
4. 対象領域の既存ADRを読み、現在有効な意思決定を把握する。
5. What、Why、Context、採用理由、必須のAlternativesを確認する。不足している必須情報は推測せず、ユーザーへ具体的に質問して回答を得る。任意情報は「未確認」と明記できる。
6. What、Why、Context、Alternatives、Consequencesを整理する。
7. テンプレートを使用してADRを作成する。
8. ADRレビューを実施し、記録漏れや矛盾を確認する。
9. レビュー結果を反映し、最終版を保存する。

## 参照

ADRを作成する際は、次のReferenceを必ず参照する。

- references/adr-principles.md
- references/adr-lifecycle.md
- references/adr-content.md
- references/adr-writing-rules.md
- references/adr-review-checklist.md

ADRを作成する際は、次のテンプレートを使用する。

- assets/adr-template.md
- 人間によるレビュー完了後に最終版をまとめる場合のみ、`assets/human-reviewed-adr-template.md`を使用する。通常のADRには`adr-template.md`を使用する。

## 人間レビュー後の専用形式

人間によるレビューが完了したことを確認した場合だけ専用テンプレートを選択する。専用形式では、レビューで確定した「なぜこのことを行ったか（Why）」と「最終的にどうなったか（What）」を必ず具体的に記録する。レビュー前の提案や通常の意思決定には専用形式を使用しない。

## 完了条件

- ADRを作成すべき変更か確認している。
- 関連する既存ADRを確認している。
- What、Why、Context、Alternatives、Consequencesを記録している。
- テンプレートに従って作成している。
- レビューが完了している。
- AIが同じ設計判断を再現できる情報が記録されている。
