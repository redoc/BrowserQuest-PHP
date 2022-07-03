use actix::{Actor, StreamHandler};
use actix::ActorContext; 




pub struct WorldServer {
    id: String,
}

impl Actor for WorldServer {
    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("hello {0}", self.id);
    }
}