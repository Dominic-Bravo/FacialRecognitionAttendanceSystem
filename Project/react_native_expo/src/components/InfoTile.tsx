import { Text, View } from "react-native";

type InfoTileProps = {
  title: string;
  value: string;
};

export function InfoTile({ title, value }: InfoTileProps) {
  return (
    <View className="min-w-[140px] flex-1 rounded-xl border border-slate-200 bg-slate-50 p-4">
      <Text className="text-xs uppercase tracking-wide text-slate-500">
        {title}
      </Text>
      <Text className="mt-1 text-lg font-semibold text-slate-900">{value}</Text>
    </View>
  );
}
