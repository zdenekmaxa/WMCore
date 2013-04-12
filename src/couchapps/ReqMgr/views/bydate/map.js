// bydate view - returns all requests sorted by RequestDate
// curl $COUCHURL/reqmgr_workload_cache/_design/ReqMgr/_view/bydate?descending=true&limit=1

function(doc) 
{
	emit(doc.RequestDate, doc);
}