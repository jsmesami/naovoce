$class_choices = $('.class-choice')
$kinds_lists = $('.kinds-list')
$kind_choices = $kinds_lists.find 'a'
$canceller = $('.canceller')
$filter = $('#filter')
$handle = $('.handle');
class Filter
	constructor: ->

	reload: (kind) ->
		@

	sneakPeek: ->
		$filter.addClass 'sneakPeek' 

	pullKinds: (e, target) ->
		$kinds_lists.hide()
		$kinds_lists.siblings(target).show()
		$class_choices.removeClass('active')
		$(e).addClass 'active'
		

@filter = F = new Filter()

	
$class_choices.on 'click', ->
	target = $(@).data 'target'
	F.pullKinds(this, target)
	false

# filter the pins
$kind_choices.on 'click', ->
	kind = $(@).data('kind')
	$filter.addClass 'filter-active'
	$handle.addClass 'filter-active' 
	$kind_choices.removeClass('active')
	$(@).addClass 'active' 

	F.reload kind
	false

# clean up the filter
 $canceller.on 'click', ->
 	$filter.removeClass 'filter-active'
 	$handle.removeClass 'filter-active'
 	$kind_choices.removeClass('active')
 	F.reload()
 	false

	