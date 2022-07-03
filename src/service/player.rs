use actix::{Actor, StreamHandler};
use actix_web::{web, Error, HttpRequest, HttpResponse};
use actix_web_actors::ws;
use actix::ActorContext; 

pub struct PlayerAgent {
    id: String,
}

impl Actor for PlayerAgent {
    type Context = ws::WebsocketContext<Self>;
    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("hello {0}", self.id);
    }
}

/// Handler for ws::Message message
impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for PlayerAgent {
    fn handle(
        &mut self,
        msg: Result<ws::Message, ws::ProtocolError>,
        _ctx: &mut Self::Context,
    ) {
        match msg {
            Ok(ws::Message::Ping(msg)) => {
                ctx.pong(&msg);
            }

            Ok(ws::Message::Text(text)) => {
                ctx.text(text);
            }

            Ok(ws::Message::Binary(bin)) => {
                ctx.binary(bin);
            }

            Ok(ws::Message::Close(reason)) => {
                ctx.close(reason);
                ctx.stop();
            }
            _ => {
                ctx.stop();
            }
        }
    }
}

impl PlayerAgent {
    fn new(id: &str) -> Self {
        Self {
            id: String::from(id)
        }
    }
}