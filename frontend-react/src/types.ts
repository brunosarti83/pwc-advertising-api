export interface ILoginForm {
  email: string;
  password: string;
}

export interface HATEOASLinkObject {
  name: string;
  method: string;
  href: string;
}

export interface IHATEOASLinks {
  self?: HATEOASLinkObject;
  actions?: HATEOASLinkObject[];
  related?: HATEOASLinkObject[];
}

export interface INewBillboard {
  width_mt: number;
  height_mt: number;
  dollars_per_day: number;
  location_id: string;
}

export interface IBillboard extends INewBillboard {
  id: string;
  location: Omit<ILocation, "id">;
  links?: IHATEOASLinks;
}

export interface INewLocation {
  address: string;
  city: string;
  state: string;
  country_code: string;
  lat: number;
  lng: number;
}

export interface ILocation extends INewLocation {
  id: string;
  links?: IHATEOASLinks;
}

export interface INewCampaign {
  name: string;
  start_date: string;
  end_date: string;
}

export interface ICampaign {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  total_dollar_amount: number;
  billboards: IBillboard[];
  links?: IHATEOASLinks;
}
