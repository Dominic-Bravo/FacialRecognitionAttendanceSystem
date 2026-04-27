import { Text, TextInput, type TextInputProps, View } from "react-native";

type FormFieldProps = TextInputProps & {
  label: string;
};

export function FormField({ label, ...props }: FormFieldProps) {
  return (
    <View className="gap-2">
      <Text className="text-sm font-medium text-slate-700">{label}</Text>
      <TextInput
        className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none"
        placeholderTextColor="#94a3b8"
        {...props}
      />
    </View>
  );
}
