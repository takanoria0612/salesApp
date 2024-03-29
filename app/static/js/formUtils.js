// js/formUtils.js
// フォームの読み取り専用状態を設定する関数
export function setFormReadOnly(isReadOnly) {
    const elements = document.querySelectorAll('#sets, #customers, #bowls, #purchase_total, #total_price, #cash_total, #card_total, #rakuten_pay, #paypay, #usd_total, #remarks');
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

    // Add the following lines to clear 楽天pay and PayPay fields
    document.getElementById('rakuten_pay').value = '';
    document.getElementById('paypay').value = '';
    document.getElementById('usd_total').value = '';
    document.getElementById('remarks').value = '';
}

// 要素のキャッシュ
// let cashTotalElement = document.getElementById('cash_total');
// let cardTotalElement = document.getElementById('card_total');
// let rakutenPayElement = document.getElementById('rakuten_pay'); // 追加
// let paypayElement = document.getElementById('paypay'); // 追加
// let usdTotalElement = document.getElementById('usd_total');
// let totalPriceElement = document.getElementById('total_price');

// 財務情報を更新する関数（キャッシュを使用）
export async function updateFinancials() {
    var cashTotal = parseFloat(document.getElementById('cash_total').value) || 0;
    var cardTotal = parseFloat(document.getElementById('card_total').value) || 0;
    var rakutenPay = parseFloat(document.getElementById('rakuten_pay').value) || 0;
    var paypay = parseFloat(document.getElementById('paypay').value) || 0;
    var usdTotal = parseFloat(document.getElementById('usd_total').value) || 0;
    var total = cashTotal + cardTotal + rakutenPay + paypay + usdTotal;
    document.getElementById('total_price').value = total;
}

export function updateFormData(data) {
    // サーバーから取得したデータをフォームに設定するロジック
    document.getElementById('sets').value = data.sets || '';
    document.getElementById('customers').value = data.customers || '';
    document.getElementById('bowls').value = data.bowls || '';
    document.getElementById('purchase_total').value = data.purchase_total || '';
    document.getElementById('cash_total').value = data.cash_total || '';
    document.getElementById('card_total').value = data.card_total || '';
    document.getElementById('rakuten_pay').value = data.rakuten_pay || ''; // 追加
    document.getElementById('paypay').value = data.paypay || 0; // 追加
    document.getElementById('usd_total').value = data.usd_total || '';
    document.getElementById('total_price').value = data.total_price || '';
    document.getElementById('remarks').value = data.remarks || '';
}

