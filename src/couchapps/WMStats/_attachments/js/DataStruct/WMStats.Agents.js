WMStats.namespace("Agents");

WMStats.Agents = function (couchData) {
    
    var _data;

    function setData(data) {
        var dataRows = data.rows;
        var rows = [];
        for (var i in dataRows) {
            var tableRow = dataRows[i].value;
            rows.push(tableRow)
        }
        _data = rows;
    }
    
    function getData() {
        return _data;
    }
    
    if (couchData) {
        setData(couchData);
    }
    
    return {
        getData: getData,
        setData: setData
    }
}