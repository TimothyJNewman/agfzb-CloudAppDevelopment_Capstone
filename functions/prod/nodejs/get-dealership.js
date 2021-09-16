/**
 * Get dealership endpoint
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
     try {
         let dbContent = cloudant.use('dealerships');
         let dbToFilter = await dbContent.list({include_docs: true})
         dbReturn = dbToFilter;
         if (params.state) {
             dbReturn.rows = dbReturn.rows.filter(row => row.doc.st === params.state);
         }
         return {
            entries: dbReturn.rows.map((row) => { return {
              id: row.doc.id,
              city: row.doc.city,
              state: row.doc.state,
              st: row.doc.st,
              address: row.doc.address,
              zip: row.doc.zip,
              lat: row.doc.lat,
              long: row.doc.long,
            }})
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