// エラーログを出力する関数
export function logError(message, error) {
    console.error(`Error: ${message}`, error);

}

// 情報ログを出力する関数
export function logInfo(message) {
    console.log(`Info: ${message}`);

}

// デバッグログを出力する関数
export function logDebug(message) {
    console.debug(`Debug: ${message}`);

}
