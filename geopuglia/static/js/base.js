var geo = {
	attribution : 'Tiles Courtesy of <a href="http://www.stamen.com/" target="_blank">Stamen</a>. Map data by © <a href="http://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>  contributors. Content data copyright © <a href="http://sit.puglia.it/" target="_blank">SIT Regione Puglia</a>',
	map : new Object,
	map_div : 'map',
	center : new OpenLayers.LonLat(1891315.3837941, 4991083.2834755),
	extent : new OpenLayers.Bounds(1453178.3377244,4801519.4533546,2324560.4600542,5266256.5852638),
	tilecacheArray : ["http://tile.stamen.com/watercolor/${z}/${x}/${y}.jpg"],
	map_proj : new OpenLayers.Projection('EPSG:900913'),
	geopuglia_div : 'panel',
	zoom : 8,

	init : function() {
		this.map = new OpenLayers.Map({
			div : this.map_div,
			controls : [new OpenLayers.Control.Attribution(), 
						new OpenLayers.Control.Zoom(), 
						//new OpenLayers.Control.LayerSwitcher(),
						new OpenLayers.Control.ScaleLine({
							maxWidth : 150,
							bottomInUnits : ''
							}), 
						new OpenLayers.Control.Navigation({ 
							dragPanOptions : { enableKinetic : true}
							}),
						new GeoPuglia({contentDiv : this.geopuglia_div})],
			projection : this.map_proj,
			restrictedExtent : this.extent
		});

		baseMap = new OpenLayers.Layer.OSM("Stamen.com Tiles", this.tilecacheArray, {
			attribution : this.attribution
		});
		
		//gsat = new OpenLayers.Layer.Google("Google Satellite", {
		//	type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22
		//});
		
		//this.map.addLayers([baseMap, gsat]);
		this.map.addLayers([baseMap]);
		this.map.setCenter(this.center, this.zoom);
	}
}

/***********************************************
 Resize
 ************************************************/
var page = {
	map : "#map",
	panel : "#panel",
	panel_closed : '#panel_closed',
	
	init : function() {
		this.setSizes();
	},

	setSizes : function() {
		$(this.map).css({
			height : $(window).height() + "px"
		});
		$(this.panel).css({
			height : ($(window).height() - parseInt(50)) + "px"
		});
	},
	
	panelUp : function() {
		$(this.panel).slideUp();
		$(this.panel_closed).show();
	},
	
	panelDown : function() {
		$(this.panel_closed).hide();
		$(this.panel).slideDown();
	}
}

/***********************************************
 DOM Ready
 ************************************************/

$(document).ready(function() {
	page.init();
	geo.init();
	$('#arrow_up').click(function() {
		page.panelUp();
	});
	$('#arrow_down').click(function() {
		page.panelDown();
	})
	// Attatch resize action to window
	$(window).resize(function() {
		page.setSizes();
	});

}); 