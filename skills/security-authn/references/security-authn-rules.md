# Security: Authentication and Session Rules

OWASP ASVS 5.0の認証・セッション管理領域（V6、V7）を対象とする。

## Password requirements (V6.2)

- パスワードは最低8文字（15文字以上を強く推奨）、最大64文字以上を許可する。
- 大文字・小文字・数字・記号の組み合わせを強制せず、すべての文字構成を許可する。
- 検証前にパスワードを切り詰めたり変更したりせず、受信した値をそのまま比較する。
- PasteとPassword Managerの自動入力を許可する。
- パスワード入力欄には`type="password"`を使用し、一時的な表示切り替えは要件に応じて許可する。
- 新しいパスワードを、対象ポリシーにおける上位3000件のよく使われるパスワードと照合する。
- 既知の漏えいパスワードデータベースと照合する。
- 定期的なパスワード変更を要求しない。漏えいまたはユーザー変更まで有効にする。
- 組織名、製品名、部署名など、Context固有の単語をパスワードに使用できないようにする。

## General authentication (V6.3)

- Brute ForceとCredential Stuffingを防ぐため、Rate Limit、Anti-automation、Adaptive Controlを実装する。
- `root`、`admin`、`sa`などのDefault Accountを無効化または削除する。
- ASVS L2ではすべてのユーザーにMFAを要求する。
- ASVS L3では、Phishing Resistanceを持つHardware Authentication（FIDO2 Hardware Key、Device-bound Passkey）を要求する。

## Authentication security (V6.4+)

- Login失敗時はGeneric Error Messageを返し、アカウント誤りとパスワード誤りを区別しない。
- Credential Recovery FlowをLoginと同じSecurity Levelで保護する。
- Backup CodeなどのLookup Secretは一度だけ使用し、CSPRNGで生成してHash化して保存する。

## Session Token fundamentals (V7.2)

- Session TokenをClientでなく信頼できるBackendで検証する。
- Static API KeyやSecretをSession Tokenとして使用せず、動的生成Tokenを使用する。
- Reference Tokenは一意で、128bit以上のEntropyを持つCSPRNGで生成する。
- 認証のたび（再認証を含む）に新しいSession Tokenを発行し、古いTokenを即時無効化する。

## Session timeout (V7.3)

- Inactivity Timeoutを強制し、Idle期間経過後は再認証を要求する。
- Absolute Maximum Session Lifetimeを強制し、最大期間経過後は再認証を要求する。
- Timeout値と設定根拠をSecurity Documentationへ記録する。

## Session termination (V7.4)

- LogoutまたはExpiration時、Reference TokenはBackendで即時無効化する。Self-contained TokenはRevocation Listまたはユーザー単位のSigning Key Rotationを使用する。
- アカウント無効化または削除時に全Sessionを終了する。
- PasswordまたはMFA変更後、他のアクティブSessionをすべて終了する選択肢を提供する。
- 管理者が個別ユーザーまたは全ユーザーのSessionを終了できるようにする。
- 認証済みページすべてに簡単にアクセスできるLogoutを提供する。

## Session abuse defenses (V7.5)

- Email、電話番号、MFA設定など機密アカウント属性を変更する前に再認証を要求する。
- ユーザーが自分のアクティブSessionを確認・終了できるようにする。
- 高度に機密性の高い取引にはStep-up Authentication（追加要素）を要求する。

## Review evidence

- Password長、文字制限、Common/Breached Password照合、Paste、Password Managerを確認したか。
- MFA強度、Default Account、Rate Limit、Credential Recoveryを検証したか。
- TokenのEntropy、一意性、再認証時のRotation、Backend検証、失効を確認したか。
- Idle/Absolute Timeoutと根拠、Logout、Password/MFA変更、アカウント削除時の全Session終了を検証したか。
- ユーザー・管理者のSession終了、再認証、Step-upの監査可能性を確認したか。
