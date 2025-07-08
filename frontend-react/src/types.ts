export interface ILoginForm {
  email: string;
  password: string;
}

export interface IBillboard {
  id: string;
  width_mt: number;
  height_mt: number;
  dollars_per_day: number;
  location: Omit<ILocation, "id">;
}

export interface ILocation {
  id: string;
  address: string;
  city: string;
  state: string;
  country_code: string;
  lat: number;
  lng: number;
}
