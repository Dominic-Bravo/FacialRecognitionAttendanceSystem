import { AuthFormCard } from "../components/AuthFormCard";
import type { AuthInput } from "../types/auth";

type LoginScreenProps = {
  input: AuthInput;
  onUpdateInput: (key: keyof AuthInput, value: string) => void;
  onLogin: () => void;
  onGoToSignup: () => void;
};

export function LoginScreen({
  input,
  onUpdateInput,
  onLogin,
  onGoToSignup,
}: LoginScreenProps) {
  return (
    <AuthFormCard
      title="Login"
      subtitle="Welcome back! Sign in to continue."
      showName={false}
      input={input}
      onUpdateInput={onUpdateInput}
      primaryCta="Sign In"
      secondaryCta="Need an account? Create one"
      onPrimaryPress={onLogin}
      onSecondaryPress={onGoToSignup}
    />
  );
}
