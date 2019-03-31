$form = $ 'form'
$amountInputs = $form.find('.donation-amount input')
$customAmountInput = $form.find('.donation-amount-custom input')
$freqInputs = $form.find('.donation-freq input')

renderQuery = (context) ->
  "https://www.darujme.cz/dar/index.php?" +
  "client=29071602&" +
  "page=checkout&" +
  "currency=CZK&" +
  "language=cz&" +
  "project=67666854&" +
  "payment_data____frequency=#{context.freq}&" +
  "ammount=#{context.amount}"

context =
  amount: 100
  freq: 28

$amountInputs.on 'change', ->
  amount = $amountInputs.filter(':checked').val()
  if amount
    $customAmountInput.val(amount)
    context.amount = amount
  else
    context.amount = $customAmountInput.val() or 100

$freqInputs.on 'change', ->
  context.freq = $freqInputs.filter(':checked').val()

$customAmountInput.on 'change', (e) ->
  amount = $(@).val()
  if amount >= 100
    $amountInputs.removeAttr('checked')
    context.amount = amount

$form.on 'submit', ->
  window.open(renderQuery(context), 'new_tab')
  false

# Reset on reload
$amountInputs.trigger 'change'
$freqInputs.trigger 'change'
