$filter = $('#filter')
$toggler = $('.toggler')
$handle = $('.handle')
$class_choices = $('.class-choice')
$kinds_lists = $('.kinds-list')
$kind_choices = $kinds_lists.find 'a'
$canceller = $('.canceller')

class Filter
	constructor: ->


	reload: (kind) ->
		@
	
	showFilter: ->
		$filter.addClass 'open'
		$handle.addClass 'open'

	pullKinds: (e, target) ->
		$kinds_lists.hide()
		$kinds_lists.siblings(target).show()
		$class_choices.removeClass('active')
		$(e).addClass 'active'

	hideFilter: (onComplete) ->
		$filter.removeClass 'open' 
		$handle.removeClass 'open'
	
	toggleFilter: ->
		$filter.toggleClass 'open' 
		$handle.toggleClass 'open'

@filter = F = new Filter()


$toggler.on 'click', ->
	F.toggleFilter()
	

$class_choices.on 'click', ->
	target = $(@).data 'target'
	F.pullKinds(this, target)

	
	

	false

$kind_choices.on 'click', ->
	kind = $(@).data('kind')
	$filter.addClass 'filter-active'
	$handle.addClass 'filter-active' 

	F.hideFilter()
	F.reload kind

	false

 $canceller.on 'click', ->
 	$filter.removeClass 'filter-active'
 	$handle.removeClass 'filter-active'

 	F.reload()

 	false
