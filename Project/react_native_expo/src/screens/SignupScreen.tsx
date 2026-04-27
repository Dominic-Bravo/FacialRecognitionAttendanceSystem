import { AuthFormCard } from "../components/AuthFormCard";
import type { AuthInput } from "../types/auth";

type SignupScreenProps = {
  input: AuthInput;
  onUpdateInput: (key: keyof AuthInput, value: string) => void;
  onSignup: () => void;
  onGoToLogin: () => void;
};

export function SignupScreen({
  input,
  onUpdateInput,
  onSignup,
  onGoToLogin,
}: SignupScreenProps) {
  return (
    <AuthFormCard
      title="Sign Up"
      subtitle="Create your account to access the dashboard."
      showName
      input={input}
      onUpdateInput={onUpdateInput}
      primaryCta="Create Account"
      secondaryCta="Already have an account? Login"
      onPrimaryPress={onSignup}
      onSecondaryPress={onGoToLogin}
    />
  );
}
