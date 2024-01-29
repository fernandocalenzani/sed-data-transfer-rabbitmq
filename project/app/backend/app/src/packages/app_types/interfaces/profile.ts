export interface ITokenUpdateData {
  token: string;
  data: string;
  date: string;
}

export interface IAddress {
  street: string;
  number: number;
  neighborhood: string;
  zipcode: string;
  city: string;
  complement: string;
  state: string;
  coords: {
    latitude: number;
    longitude: number;
  };
}

export interface IPermissions {
  userType: string;
  access: string[];
}

export interface IFile {
  _id: string;
  url: string;
  fieldname: string;
  originalname: string;
  encoding: string;
  mimetype: string;
  destination: string;
  filename: string;
  path: string;
  size: number;
  buffer: Uint8Array | number[];
}

export interface IUserAuth {
  _id: string;
  email: string;
  name: string;
}
