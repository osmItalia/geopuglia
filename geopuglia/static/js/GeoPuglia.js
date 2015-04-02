/**
 * @author Alessandro
 */

/**
 * Class: OpenLayers.Control.GeoPuglia
 *
 * Inherits from:
 *  - <OpenLayers.Control>
 */
GeoPuglia = OpenLayers.Class(OpenLayers.Control, {

	confinicomunali : new Object,

	confiniprovinciali : new Object,

	edifici : new Object,
	
	point : new Object,
	
	line : new Object,
	
	polygon : new Object,
	
	map_proj : new OpenLayers.Projection('EPSG:900913'),

	data_proj : new OpenLayers.Projection('EPSG:4326'),

	wfs_url : '/wfs_proxy/?url=http://ms.piemapping.com/?map=/ms/mapfiles/eventmanager.map',
	
	minScale : 3500,


	/**
	 * Constructor: GeoPuglia
	 * Create a new control to deal SIT Puglia data
	 *
	 */
	initialize : function(options) {
		OpenLayers.Control.prototype.initialize.apply(this, arguments);
		this.div = OpenLayers.Util.getElement(this.contentDiv);
	},

	/**
	 * Method: draw
	 * Add the elements to the HTML page
	 *
	 */
	draw : function() {
		OpenLayers.Control.prototype.draw.apply(this);
		this.wmsPanel();
		this.wfsPanel();
		//this.addWfsLayers();
	},

	wmsPanel : function() {
		//
		var wms_div = document.createElement('div');
		wms_div.id = 'wms_panel_div';
		var wms_h2 = document.createElement('h2');
		wms_h2.innerHTML = 'WMS Layers';
		// provinciali
		var confini_provinciali_p = document.createElement('p');
		var confini_provinciali = document.createElement('input');
		confini_provinciali.type = 'checkbox';
		confini_provinciali.name = 'Provinces';
		confini_provinciali.value = 'confiniprovinciali';
		confini_provinciali.id = 'confiniprovinciali';
		var confini_provinciali_lable = document.createElement('lable');
		confini_provinciali_lable.htmlFor = 'confiniprovinciali';
		confini_provinciali_lable.innerHTML = ' Provinces';
		confini_provinciali_p.appendChild(confini_provinciali);
		confini_provinciali_p.appendChild(confini_provinciali_lable);
		// comunali
		var confini_comunali_p = document.createElement('p');
		var confini_comunali = document.createElement('input');
		confini_comunali.type = 'checkbox';
		confini_comunali.name = 'Municipalities';
		confini_comunali.value = 'confinicomunali';
		confini_comunali.id = 'confinicomunali';
		var confini_comunali_lable = document.createElement('lable');
		confini_comunali_lable.htmlFor = 'confinicomunali';
		confini_comunali_lable.innerHTML = ' Municipalities';
		confini_comunali_p.appendChild(confini_comunali);
		confini_comunali_p.appendChild(confini_comunali_lable);
		// edifici
		var edifici_p = document.createElement('p');
		var edifici = document.createElement('input');
		edifici.type = 'checkbox';
		edifici.name = 'Edifici';
		edifici.value = 'edifici';
		edifici.id = 'edifici';
		var edifici_lable = document.createElement('lable');
		edifici_lable.htmlFor = 'edifici';
		edifici_lable.innerHTML = ' Buildings';
		edifici_p.appendChild(edifici);
		edifici_p.appendChild(edifici_lable);
		//
		wms_div.appendChild(wms_h2);
		wms_div.appendChild(confini_provinciali_p);
		wms_div.appendChild(confini_comunali_p);
		wms_div.appendChild(edifici_p);
		this.div.appendChild(wms_div);
		// events
		OpenLayers.Event.observe(confini_comunali, 'click', this.toogleConfiniComunali.bind(this));
		OpenLayers.Event.observe(confini_provinciali, 'click', this.toogleConfiniProvinciali.bind(this));
		OpenLayers.Event.observe(edifici, 'click', this.toogleEdifici.bind(this));
	},

	wfsPanel : function() {
		var geometry_type = ['POINT', 'LINE', 'POLYGON'];
		var succes_function = [this.populatePoint, this.populateLine, this.populatePolygon];
		for (var i = 0, end = geometry_type.length; i < end; i++) {
			OpenLayers.Request.GET({
				url : '/get_layers/',
				params : {
					geometry_type : geometry_type[i]
				},
				scope : this,
				success : succes_function[i]
			});
		}
		// point
		this.point_layers_p = document.createElement('p');
		this.point_layers_h2 = document.createElement('h2');
		this.point_layers_h2.innerHTML = 'Point Layers';
		this.point_layers_loader = document.createElement('img');
		this.point_layers_loader.src = '/static/image/panel-loader.gif';
		this.point_layers_p.appendChild(this.point_layers_h2);
		this.point_layers_p.appendChild(this.point_layers_loader);
		// line
		this.line_layers_p = document.createElement('p');
		this.line_layers_h2 = document.createElement('h2');
		this.line_layers_h2.innerHTML = 'Line Layers';
		this.line_layers_loader = document.createElement('img');
		this.line_layers_loader.src = '/static/image/panel-loader.gif';
		this.line_layers_p.appendChild(this.line_layers_h2);
		this.line_layers_p.appendChild(this.line_layers_loader);
		// polygon
		this.polygon_layers_p = document.createElement('p');
		this.polygon_layers_h2 = document.createElement('h2');
		this.polygon_layers_h2.innerHTML = 'Polygon Layers';
		this.polygon_layers_loader = document.createElement('img');
		this.polygon_layers_loader.src = '/static/image/panel-loader.gif';
		this.polygon_layers_p.appendChild(this.polygon_layers_h2);
		this.polygon_layers_p.appendChild(this.polygon_layers_loader);
		//
		this.div.appendChild(this.point_layers_p);
		this.div.appendChild(this.line_layers_p);
		this.div.appendChild(this.polygon_layers_p);
	},

	/**
	 * 
	 */
	addWfsLayers: function() {
		this.point = new OpenLayers.Layer.Vector("Points", {
			strategies : [new OpenLayers.Strategy.BBOX()],
			protocol : new OpenLayers.Protocol.HTTP({
				url : this.wfs_url,
				params : {
					service : "WFS",
					request : "GetFeature",
					srs : "EPSG:3857",
					version : "1.1.0",
					typeName : "point"
				},
				format : new OpenLayers.Format.GML.v3()
			}),
			filter : new OpenLayers.Filter.Comparison({
			type : OpenLayers.Filter.Comparison.EQUAL_TO,
			property : "code",
			value : councilName
		}),
			projection : this.map_proj,
			visibility : true,
			minScale : this.minScale,
		});
		this.map.addLayer(this.point);
		// events
		//this.street_layer.events.register('loadstart', this.street_layer, this.showLoader);
		//this.street_layer.events.register('loadend', this.street_layer, this.hideLoader);
	},
	
	/**
	 *
	 */
	populateSelect : function(field, options_array) {
		field.options[field.options.length] = new Option('-- Select a Layer --', -1);
		for (var i = 0, end = options_array.length; i < end; i++) {
			field.options[field.options.length] = new Option('    ' + options_array[i].fields.description, options_array[i].fields.code);
		}
	},

	/**
	 *
	 */
	populatePoint : function(response) {
		try {
			var response = eval('(' + response.responseText + ')');
		} catch (e) {
			var response = false;
		}
		this.pointSelect = document.createElement('select');
		this.pointSelect.className = 'layerSelect';
		this.pointSelect.id = 'pointSelect';
		this.populateSelect(this.pointSelect, response);
		this.point_layers_p.removeChild(this.point_layers_loader);
		this.point_layers_p.appendChild(this.pointSelect);
	},

	/**
	 *
	 */
	populateLine : function(response) {
		try {
			var response = eval('(' + response.responseText + ')');
		} catch (e) {
			var response = false;
		}
		this.lineSelect = document.createElement('select');
		this.lineSelect.className = 'layerSelect';
		this.lineSelect.id = 'lineSelect';
		this.populateSelect(this.lineSelect, response);
		this.line_layers_p.removeChild(this.line_layers_loader);
		this.line_layers_p.appendChild(this.lineSelect);
	},

	/**
	 *
	 */
	populatePolygon : function(response) {
		try {
			var response = eval('(' + response.responseText + ')');
		} catch (e) {
			var response = false;
		}
		this.polygonSelect = document.createElement('select');
		this.polygonSelect.className = 'layerSelect';
		this.polygonSelect.id = 'polygonSelect';
		this.populateSelect(this.polygonSelect, response);
		this.polygon_layers_p.removeChild(this.polygon_layers_loader);
		this.polygon_layers_p.appendChild(this.polygonSelect);
	},

	/**
	 *
	 */
	toogleConfiniComunali : function() {
		if (this.confinicomunali.map == null) {
			this.confinicomunali = new OpenLayers.Layer.WMS("confini_comunali", "/tc/", {
				layers : 'confini_comunali',
				format : 'image/png',
				srs : 'EPSG:900913',
				isBaseLayer : false,
				transparent : true
			});
			this.map.addLayer(this.confinicomunali);
		} else {
			this.confinicomunali.destroy();
		}
	},

	/**
	 *
	 */
	toogleConfiniProvinciali : function() {
		if (this.confiniprovinciali.map == null) {
			this.confiniprovinciali = new OpenLayers.Layer.WMS("confini_provinciali", "/tc/", {
				layers : 'confini_provinciali',
				format : 'image/png',
				srs : 'EPSG:900913',
				isBaseLayer : false,
				transparent : true
			});
			this.map.addLayer(this.confiniprovinciali);
		} else {
			this.confiniprovinciali.destroy();
		}
	},

	/**
	 *
	 */
	toogleEdifici : function() {
		if (this.edifici.map == null) {
			this.edifici = new OpenLayers.Layer.WMS("edifici", "/tc/", {
				layers : 'edifici',
				format : 'image/png',
				srs : 'EPSG:900913',
				isBaseLayer : false,
				transparent : true
			});
			this.map.addLayer(this.edifici);
		} else {
			this.edifici.destroy();
		}
	},

	/** @final @type String */
	CLASS_NAME : "GeoPuglia"
});
