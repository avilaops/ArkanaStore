use mongodb::{Client, Database as MongoDatabase};

pub struct Database {
    pub db: MongoDatabase,
}

impl Database {
    pub async fn new(uri: &str, db_name: &str) -> Result<Self, mongodb::error::Error> {
        let client = Client::with_uri_str(uri).await?;
        let db = client.database(db_name);

        // Test connection
        db.run_command(mongodb::bson::doc! { "ping": 1 }, None)
            
    .await?;

        Ok(Self { db })
}

    pub fn products(&self) -> mongodb::Collection<mongodb::bson::Document> {
        self.db.collection("products")
}

    pub fn orders(&self) -> mongodb::Collection<mongodb::bson::Document> {
        self.db.collection("orders")
}

    pub fn customers(&self) -> mongodb::Collection<mongodb::bson::Document> {
        self.db.collection("customers")
}

    pub fn carts(&self) -> mongodb::Collection<mongodb::bson::Document> {
        self.db.collection("carts")
    }
}
