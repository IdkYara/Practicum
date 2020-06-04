function initMap() {
    let osmLayer = new ol.layer.Tile({
        source: new ol.source.OSM(),
        title: 'OSM basemap',
        type: 'base',
        visible: false
    });
    //    
    //    let stamenLayer =new ol.layer.Tile({
    //        source: new ol.source.Stamen({
    //            layer: 'watercolor'
    //        }),
    //        title: 'Stamen basemap',
    //        type: 'base',
    //        visible: false
    //    });

    let darkmapesri = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/' +
                'World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
            minZoom: 3,

        }),
        title: 'Darkmap Esri',
        type: 'base',
        visible: true
    });



    map = new ol.Map({
        target: 'map',
        layers: [osmLayer, darkmapesri],
        view: WereldView,
        maxzoom: 2

    });

    /**
     * Elements that make up the popup.
     */
    let container = document.getElementById('popup');
    let content = document.getElementById('popup-content');
    let closer = document.getElementById('popup-closer');


    /**
     * Create an overlay to anchor the popup to the map.
     */
    let overlay = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });

    map.addOverlay(overlay);

    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closer.onclick = function () {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
    };

    // vectorSource.addFeatures(new ol.format.GeoJSON().readFeatures(gemeentenJSON, {
    //     dataProjection: 'EPSG:4326',
    //     featureProjection: 'EPSG:3857'
    // }));

    let WMSnaam1DBSource = new ol.source.ImageWMS({

        url: 'http://gmd.has.nl/geoserver/engineer_1920_981221541/wms',
        params: {
            'LAYERS': 'eng:aantal_immigratie_en_conflicten_per_land_per_jaar' //omgevingnaam:laagnaam
        }
    });
    let WMSnaam1DBLayer = new ol.layer.Image({
        source: WMSnaam1DBSource,
        title: 'WMSlaag1',
        type: 'overlay',
        visible: true

    });

    let WMSnaam2DBSource = new ol.source.ImageWMS({

        url: 'https://gmd.has.nl/geoserver/engineer_1920_981221541/wms',
        params: {
            'LAYERS': 'engineer_1920_981221541:conflicten' //omgevingnaam:laagnaam
        }
    });
    let WMSnaam2DBLayer = new ol.layer.Image({
        source: WMSnaam2DBSource,
        title: 'WMSlaag2',
        type: 'overlay',
        visible: true

    });


    map.addLayer(WMSnaam1DBLayer);
    map.addLayer(WMSnaam2DBLayer);

    //    //Feature waarin hij icoon laat zien op kaart
    //    let NederlandFeature = new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat([5.104480, 52.092876])));
    //    
    //    let vectorSource = new ol.source.Vector();
    //    let vectorLayer = new ol.layer.Vector({
    //        source: vectorSource,
    //        style: new ol.style.Style({
    //                image: new ol.style.Icon(/** @type {module:ol/style/Icon~Options} */ ({
    //                anchor: [0.5, 0.5],
    //                anchorXUnits: 'fraction',
    //                anchorYUnits: 'fraction',
    //                opacity: 0.90,
    //                src: 'images/netherlandsflag.png'
    //              })),
    //              stroke: new ol.style.Stroke({
    //                width: 3,
    //                color: [255, 0, 0, 1]
    //              }),
    //              fill: new ol.style.Fill({
    //                color: [0, 255, 0, 0.3]
    //              })
    //            })
    //    });
    //    vectorSource.addFeature(NederlandFeature);
    //    map.addLayer(vectorLayer);

    map.on('singleclick', function (evt) {
        let viewResolution = /** @type {number} */ (WereldView.getResolution());
        let getFeatureInfoUrl = WMSnaam1DBSource.getGetFeatureInfoUrl(
            evt.coordinate, viewResolution, 'EPSG:3857', {
                'INFO_FORMAT': 'application/json'
            });
        if (getFeatureInfoUrl) {
            // document.getElementById('info').innerHTML =
            //      '<iframe seamless src="' + url + '"></iframe>';
            console.log(getFeatureInfoUrl);
            $.ajax({
                url: getFeatureInfoUrl,
                dataType: 'json'
            }).done(function (data) {
                console.log(data.features[0].properties);
                $("#landnaam").html(data.features[0].properties.landnaam);
                $("#aantal_immigratie").html(data.features[0].properties.aantal_immigratie);
                $("#aantal_conflicten").html(data.features[0].properties.aantal_conflicten);

                //           content.innerHTML = data.features[0].properties.bouwjaar;
                overlay.setPosition(evt.coordinate);

            });
        }
    });

    // map.on('click', function(evt) {
    //     let selFeature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
    //         return feature
    //     });
    //     if (selFeature) {
    //         content.innerHTML = "Bodemtype: " + selFeature.values_.bodemtype;
    //         overlay.setPosition(evt.coordinate);
    //     } else {
    //         overlay.setPosition(undefined);
    //         overlay.blur;
    //     }
    // });


    //    let postData = {
    //        url: 'http://gmd.has.nl:8080/geoserver/dyla/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dyla:bodemkaart&outputFormat=application%2Fjson&srsName=EPSG:4326'
    //    };

    //    $.ajax({
    //        url: 'php/geoproxycurl.php',
    //        dataType: 'json',
    //        data: postData,
    //        method: 'post'
    //    }).done(function(data) { 
    //        vectorSource.addFeatures(new ol.format.GeoJSON().readFeatures(data, {
    //            dataProjection: 'EPSG:4326',
    //            featureProjection: 'EPSG:3857'
    //            }));
    //    });

    // var layerSwitcher = new ol.control.LayerSwitcher({
    //     tipLabel: 'Légende', // Optional label for button
    //     groupSelectStyle: 'children' // Can be 'children' [default], 'group' or 'none'
    // });
    // map.addControl(layerSwitcher);

    buildLayerSwitcher();

    $("input[name='basemapRadio']").on('change', function () { // als er op een radiobutton geklikt is
        let selectedLayer = $("input[name='basemapRadio']:checked").val(); // welke laag is geselecteerd?
        $.each(mapLayers, function (i, layer) { // doorloop alle lagen van de kaart
            if (i == selectedLayer) { // als de laag de geselecteerde laag is
                layer.setVisible(true); // maak de laag zichtbaar
            } else { // als de laag niet de geselecteerde laag is
                if (layer.values_.type == 'base') { // en het is een basemap
                    layer.setVisible(false); // maak hem dan niet zichtbaar
                }
            }
        });
    });

} //end of Initmap

//function ganaaradam() {
//    map.setView(amsterdamView);
//}


function switchOverlay(layerNr) {
    // aan- of uitzetten van een laag als checkbox verandert
    if (mapLayers[layerNr].values_.visible) { // is de laag zichtbaar?
        mapLayers[layerNr].setVisible(false); // zet de laag uit

    } else { // anders
        mapLayers[layerNr].setVisible(true); // zet de laag aan
    }
}

function buildLayerSwitcher() {
    $('#overlayselectlist').html(""); // leegmaken van de overlay lagenswitcher op de pagina
    $('#basemapselectlist').html("");
    mapLayers = map.getLayers().getArray(); // ophalen van alle lagen van e kaart
    $.each(mapLayers, function (i, layer) { // voor elke laag
        if (layer.values_.type == 'overlay') { // als het een overlag-laag is
            // opbouwen van de HTML code voor een checkbox
            let liTekst = '<li><input type="checkbox" onchange="switchOverlay(';
            liTekst += i + ')" id="overlay' + i + '"';
            if (layer.values_.visible) { //als de laag zichtbaar is moet de checkbox aangevinkt zijn.
                liTekst += " checked"
            }
            liTekst += '><label for="overlay' + i + '">' + layer.values_.title + '</label>' + '</li>' // zorgen dat er ook op de tekst geklikt kan worden om de checkbox aan- of uit te vinken
            $('#overlayselectlist').append(liTekst); // voeg de checkbox toe aan de pagina 
        } else {
            if (layer.values_.type == 'base') { // als het een basemap-laag is
                // opbouwen van de HTML code voor een radio button
                let liTekst = '<li><input type="radio" name="basemapRadio"';
                liTekst += ' id="base' + i + '" value="' + i + '"';
                if (layer.values_.visible) { //als de laag zichtbaar is moet de radio button aangevinkt zijn.
                    liTekst += " checked"
                }
                liTekst += '><label for="base' + i + '">' + layer.values_.title + '</label>' + '</li>' // zorgen dat er ook op de tekst geklikt kan worden om de radio button aan- of uit te vinken
                $('#basemapselectlist').append(liTekst); // voeg de radio button toe aan de pagina 
            }
        }
    });


}
