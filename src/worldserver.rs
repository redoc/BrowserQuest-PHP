use actix::{Actor, StreamHandler};
use actix::ActorContext; 




pub struct PlayerAgent {
    id: String,
}

impl Actor for PlayerAgent {
    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("hello {0}", self.id);
    }
}