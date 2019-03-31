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
  $nano = $('.nano')

  $window.resize ->
    $userInfoHeight = $('#user-info').innerHeight()
    $contentHeight = $(window).height() - $userInfoHeight
    $kindListHeight = $('.kinds-list').height()

    # fill up the vertical space with the map
    $elem.css 'min-height', "#{ Math.max $window.outerHeight() - $userInfoHeight, 320 }px"

    $('.gold').css('min-height', $contentHeight + 'px')
    # for all nanos outside filter
    if not $nano.parents('.filter') or $contentHeight < $kindListHeight
      $nano.css('min-height', $contentHeight + 'px')
      $nano.css({'max-height': $contentHeight + 'px'})
    # for nano in filter and only if the content height is higher than the filter content
    else if $kindListHeight != null
      $nano.css('min-height', ( $kindListHeight + 50) + 'px')
      $nano.css({'max-height': ( $kindListHeight + 50) + 'px'})
    # normal "full" height
    else
      $nano.css('min-height', ( $contentHeight) + 'px')
      $nano.css({'max-height': ( $contentHeight) + 'px'})

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


# open || close: mobile menu/panel/filter
$menu_toggle = $('.ham_toggle')
$panel_toggle = $('.panel_toggle')
$filter_toogle = $('.toggler')
$body = $('body')
$filter = $('#filter')


# close all extra panels, menus and such
close_all = (e) ->
  if e != 'panel_open'
    $body.removeClass 'panel_open'
  if e != 'filter_open'
    $body.removeClass 'filter_open'
  if e != 'menu_open'
    $body.removeClass 'menu_open'


# on huge monitors open the filter automagically
if $(window).width() > 1300
  actual = 'filter_open'
  close_all actual
  $body.toggleClass actual


# open mobile menu, close everything else
$menu_toggle.on 'click', ->
  actual = 'menu_open'
  close_all actual
  # toggle the menu
  $body.toggleClass actual


# open mobile menu, close everything else
$panel_toggle.on 'click', ->
  actual = 'panel_open'
  close_all actual
  # toggle the right panel
  $body.toggleClass actual


$filter_toogle.on 'click', ->
  actual = 'filter_open'
  close_all actual
  $body.toggleClass actual


# MOBILE SNIFFING
# os detection - mobile-detect.js
$md = new MobileDetect(window.navigator.userAgent);
# if we meet an old browser show them the link to the app store instead of the broken web layout
if $md.is('Samsung') then $('#getApp').css('display', 'flex')
$body.addClass('isOS_'+$md.os() + ' ' + 'isPhone_' + $md.mobile())
