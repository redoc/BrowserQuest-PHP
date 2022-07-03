mod cli;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = cli::parse();
    // println!("cli args: {:?}", args);
    if args.cmd_web {
        return cli::start_web(&args).await;
    } else if args.cmd_lobby {
        return cli::start_lobby(&args).await;
    } else {
        panic!("missing subcommand");
    }
}