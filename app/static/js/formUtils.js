// js/formUtils.js
// フォームの読み取り専用状態を設定する関数
export function setFormReadOnly(isReadOnly) {
    const elements = document.querySelectorAll('#sets, #customers, #bowls, #purchase_total, #total_price, #cash_total, #card_total, #usd_total, #remarks');
    elements.forEach(element => {
        element.readOnly = isReadOnly;
    });

    // readOnlyの場合は送信ボタンを無効化
    document.querySelector('input[type="submit"]').disabled = isReadOnly;
}

// フォームデータをクリアする関数
export function clearFormData() {
    document.getElementById('sets').value = '';
    document.getElementById('customers').value = '';
    document.getElementById('bowls').value = '';
    document.getElementById('purchase_total').value = '';
    document.getElementById('total_price').value = '';
    document.getElementById('cash_total').value = '';
    document.getElementById('card_total').value = '';
    document.getElementById('usd_total').value = '';
    document.getElementById('remarks').value = '';
}

// 要素のキャッシュ
let cashTotalElement = document.getElementById('cash_total');
let cardTotalElement = document.getElementById('card_total');
let usdTotalElement = document.getElementById('usd_total');
let totalPriceElement = document.getElementById('total_price');

// 財務情報を更新する関数（キャッシュを使用）
export function updateFinancials() {
    var cashTotal = parseFloat(cashTotalElement.value) || 0;
    var cardTotal = parseFloat(cardTotalElement.value) || 0;
    var usdTotal = parseFloat(usdTotalElement.value) || 0;
    var total = cashTotal + cardTotal + usdTotal;
    totalPriceElement.value = total;
}

export function updateFormData(data) {
    // サーバーから取得したデータをフォームに設定するロジック
    document.getElementById('sets').value = data.sets || '';
    document.getElementById('customers').value = data.customers || '';
    document.getElementById('bowls').value = data.bowls || '';
    document.getElementById('purchase_total').value = data.purchase_total || '';
    document.getElementById('total_price').value = data.total_price || '';
    document.getElementById('cash_total').value = data.cash_total || '';
    document.getElementById('card_total').value = data.card_total || '';
    document.getElementById('usd_total').value = data.usd_total || '';
    document.getElementById('remarks').value = data.remarks || '';
}

