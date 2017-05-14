@Naovoce = {} # Application namespace


class JsonStorage
	###
	Provides getting and setting JSON-serialized objects in localStorage,
	which otherwise supports key-value strings storage only.
	###
	constructor: (namespace) ->
		if Storage?
			storage = localStorage

			@getObject = (name) ->
				data = storage.getItem(namespace)
				if data then JSON.parse(data)[name] else null

			@setObject = (name, val) ->
				data = storage.getItem(namespace)
				data = if data then JSON.parse(data) else {}
				data[name] = val
				storage.setItem namespace, JSON.stringify data

		else
			@getObject = @setObject = -> null


@Naovoce.storage = new JsonStorage('naovoce')


# Enhance strings with truncete method.
String::truncate = (n) ->
	@substr(0, n - 1).trim() + ((if @length > n then "&hellip;" else ""))


$.fn.fillViewport = ->
	###
	jQuery plugin for stretching an element height to fill down the browser window
	###
	$window = $(window)
	$elem = this
	$userInfoHeight = $('#user-info').innerHeight()
	$nano = $('.nano')

	$window.resize ->
		$elem.css 'min-height', "#{ Math.max $window.outerHeight() - $userInfoHeight, 320 }px"
		$('.gold,.nano').css('min-height', ($(window).height() - $('#user-info').height()) + 'px')
		$nano.nanoScroller()
	.trigger 'resize'


$('.inputfile').each ->
	###
    File input field masquerade
	###
	$input = $ @
	$label = $input.next 'label'
	labelVal = $label.html()

	$input.on 'change', (e) ->

		if e.target.value
			fileName = e.target.value.split('\\').pop()

		$label.html if fileName? then fileName else labelVal


$('#main-content').fillViewport()

# open || close mobile menu & panel & stuff
$ham_toggle = $('.ham_toggle')
$panel_toggle = $('.panel_toggle')
$wurst = $('#wurst')
$body = $('body')

$ham_toggle.on 'click', ->
	$wurst.toggleClass 'open'
	$body.toggleClass 'mobile_menu_open'
	
$panel_toggle.on 'click', ->
	$body.toggleClass 'mobile_panel_closed'
