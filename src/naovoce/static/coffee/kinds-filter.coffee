$filter = $('#filter')
$toggler = $filter.find '.toggler'
$canceller = $filter.find '.canceller'
$class_choices = $('.class-choice')
$kinds_lists = $('.kinds-list')
$kind_choices = $kinds_lists.find 'a'


class Filter
	constructor: ->
		@speed = 200
		@classes_pulled = false
		@kinds_pulled = false

	reload: (kind) ->
		@

	pullClasses: ->
		$filter.animate right: "-120px",
			duration: @speed
			complete: =>
				@classes_pulled = true

	pullKinds: ->
		if not @kinds_pulled
			$filter.animate right: "0px",
				duration: @speed
				complete: =>
					@kinds_pulled = true

	hideFilter: (onComplete) ->
		$filter.animate right: "-170px",
			duration: @speed
			complete: =>
				@classes_pulled = false
				@kinds_pulled = false
				onComplete?()


@filter = F = new Filter()


$toggler.on 'click', ->
	console.log F.classes_pulled
	if not F.classes_pulled
		F.pullClasses()
	else
		F.hideFilter()

	false

$class_choices.on 'click', ->
	target = $(@).data 'target'

	$kinds_lists.hide()
	$kinds_lists.siblings(target).show()

	F.pullKinds()

	false

$kind_choices.on 'click', ->
	kind = $(@).data('kind')

	F.hideFilter ->
		$filter.addClass 'filter-active'
		F.reload kind

	false

$canceller.on 'click', ->
	$filter.removeClass 'filter-active'

	F.hideFilter ->
		F.reload()

	false
