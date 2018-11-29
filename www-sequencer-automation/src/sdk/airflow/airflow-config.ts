export class AirflowConfig {
  private static path = '//localhost:8080';
  private static api = '/api/experimental/';

  public static setBaseURL(url: string = '/'): void {
    AirflowConfig.path = `${url}${this.api}`;
  }

  public static getPath(): string {
    AirflowConfig.path = `${this.path}${this.api}`;
    return AirflowConfig.path;
  }
}
