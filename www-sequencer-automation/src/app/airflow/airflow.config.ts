export interface AirflowModuleConfigOptions {
  host: string;
  port: string;
  apiEndPoint: string;
}

export class AirflowModuleConfigOptionsDefaults {
  public apiEndPoint: string;
  public host: string;
  public port: string;

  constructor(config: AirflowModuleConfigOptions) {
    this.apiEndPoint = config.apiEndPoint;
    this.host = config.host;
    this.port = config.port;
  }
}
