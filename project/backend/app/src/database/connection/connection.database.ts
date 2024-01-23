import lodash from "lodash";
import mongoose, { Connection, Mongoose, set } from "mongoose";

class DBConnection {
  private instance: Mongoose | undefined;

  async createConnection(url: string) {
    try {
      this.instance = set("strictQuery", true);
      this.instance = await mongoose.connect(url);
      await this.eventEmitter(this.instance.connection);
    } catch (err) {
      console.error(err);
    }
  }

  private async eventEmitter(db: Connection) {
    console.info(`DATABASE BASE     | host: ${db.host}`);
    console.info(`DATABASE BASE     | port: ${db.port}`);
    console.info(`DATABASE BASE     | name: ${db.name}`);
    console.info(`DATABASE BASE     | user: ${db.user}`);
    console.info(
      `DATABASE BASE     | connections: ${
        this.instance ? this.instance.connections.length : 0
      }`
    );
    console.info(
      `DATABASE BASE     | status: ${this.getStatus(Number(db.readyState))}`
    );
    console.info(`DATABASE BASE     | plugins: ${db.plugins}`);

    if (!lodash.isEmpty(db)) {
      db.on("connecting", () => {
        console.warn("DATABASE BASE     | Connecting to database!");
      });

      db.on("connected", () => {
        console.warn(`DATABASE BASE     | Connected successfully`);
      });

      db.on("open", () => {
        console.warn("DATABASE BASE     | Open connection to database!");
      });

      db.on("disconnecting", () => {
        console.warn("DATABASE BASE     | Disconnecting to database!");
      });

      db.on("disconnected", () => {
        console.warn("DATABASE BASE     | Lost connection to database!");
      });

      db.on("close", () => {
        console.warn("DATABASE BASE     | Close connection to database!");
      });

      db.on("reconnected", () => {
        console.warn("DATABASE BASE     | Reconnected to database!");
      });

      db.on("error", (err) => {
        console.warn("DATABASE BASE     | Error connecting to database:", err);
      });

      db.on("fullsetup", () => {
        console.warn("DATABASE BASE     | Fullsetup to database!");
      });

      db.on("all", () => {
        console.warn("DATABASE BASE     | All to database!");
      });
    }
  }

  private getStatus(code: number) {
    let status: string;
    switch (code) {
      case 0:
        status = "disconnected";
        break;
      case 1:
        status = "connected";

        break;
      case 2:
        status = "connecting";

        break;
      case 3:
        status = "disconnecting";

        break;
      case 99:
        status = "uninitialized";

        break;

      default:
        status = "no status code";

        break;
    }

    return status;
  }
}

export const dbConnection = new DBConnection();
