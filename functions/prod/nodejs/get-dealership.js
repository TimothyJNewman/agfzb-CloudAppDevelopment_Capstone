/**
 * Get dealership endpoint
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         //url: params.COUCH_URL,
         //plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
        url: "https://dde8132b-8051-43bb-8826-e3e668959555-bluemix.cloudantnosqldb.appdomain.cloud",
        plugins: { iamauth: { iamApiKey: "EFhAv_KvwaGMZlmbnP9UkM9Gj-jjm1m8iJwdEmlTtba8" } }
     });
 
     try {
         let dbContent = cloudant.use('dealerships');
         let dbToFilter = await dbContent.list({include_docs: true})
         dbReturn = dbToFilter;
         if (params.state) {
             dbReturn.rows = dbReturn.rows.filter(row => row.doc.st === params.state);
         }
         if (params.dealerId) {
             dbReturn.rows = dbReturn.rows.filter(row => row.doc.id === params.dealerId);
         }
         return {
            rows: dbReturn.rows.map((row) => { 
            return {
            doc: {
              id: row.doc.id,
              city: row.doc.city,
              state: row.doc.state,
              st: row.doc.st,
              address: row.doc.address,
              zip: row.doc.zip,
              lat: row.doc.lat,
              long: row.doc.long,
              full_name: row.doc.full_name,
              short_name: row.doc.short_name
            }
            }
            })
         };
     } catch (error) {
         if (error.code == 404) {
             return error.code + ": The database is empty";
         } else if (error.code == 500) {
             return error.code + ": Something went wrong on the server";
         }
         return { error: error.description };
     }
 
 }