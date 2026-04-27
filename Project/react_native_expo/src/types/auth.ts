export type Screen = "login" | "signup" | "dashboard";

export type AuthInput = {
  name: string;
  email: string;
  password: string;
};

export const initialAuthInput: AuthInput = {
  name: "",
  email: "",
  password: "",
};
