import argparse
import ipaddress


def parse_route_line(line):
    """'ip route CIDR IFACE auto !COMMENT' -> (network, iface, auto, comment)."""
    line = line.strip()
    if not line or not line.startswith('ip route '):
        return None
    parts = line.split(None, 5)
    if len(parts) < 3:
        return None
    cidr = parts[2]
    iface = parts[3] if len(parts) > 3 else ''
    auto = parts[4] if len(parts) > 4 else ''
    comment = parts[5] if len(parts) > 5 else ''
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        return None
    return network, iface, auto, comment


def merge_routes(files):
    groups = {}
    per_file_counts = []

    for filepath in files:
        count = 0
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for line in f:
                result = parse_route_line(line)
                if result:
                    count += 1
                    net, iface, auto, comment = result
                    key = (net.version, iface, auto)
                    groups.setdefault(key, {}).setdefault(net, comment)
        if not count:
            raise ValueError(f"В файле {filepath} нет маршрутов")
        per_file_counts.append((filepath, count))

    merged = []
    for (_, iface, auto), routes in groups.items():
        originals = iter(sorted(routes, key=lambda n: (int(n.network_address), n.prefixlen)))
        original = next(originals, None)
        for net in ipaddress.collapse_addresses(routes):
            comments = []
            while original is not None and original.network_address <= net.broadcast_address:
                for label in routes[original].lstrip('!').split(','):
                    if label and label not in comments:
                        comments.append(label)
                original = next(originals, None)
            comment = '!' + ','.join(comments) if comments else ''
            merged.append((net, (iface, auto, comment)))

    merged.sort(key=lambda item: (
        item[0].version, int(item[0].network_address), item[0].prefixlen, item[1]
    ))
    return merged, per_file_counts


def main():
    parser = argparse.ArgumentParser(
        description='Объединяет файлы маршрутов Keenetic, убирает дубли и объединяет подсети без лишних адресов.'
    )
    parser.add_argument('files', nargs='+', help='Входные файлы маршрутов')
    parser.add_argument('-o', '--output', default='merged-routes.txt',
                        help='Выходной файл (по умолчанию: merged-routes.txt)')
    args = parser.parse_args()

    try:
        routes, per_file_counts = merge_routes(args.files)
    except (OSError, ValueError) as e:
        parser.exit(1, f"Ошибка объединения: {e}\n")

    total_before = sum(c for _, c in per_file_counts)
    print("Входные файлы:")
    for filepath, count in per_file_counts:
        print(f"  {filepath}: {count} записей")
    print(f"  Итого: {total_before} записей\n")

    with open(args.output, 'w', encoding='utf-8') as f:
        for net, (iface, auto, comment) in routes:
            parts = ['ip route', str(net), iface, auto, comment]
            f.write(' '.join(p for p in parts if p) + '\n')

    total_after = len(routes)
    print(f"Результат: {total_after} записей → {args.output}")
    print(f"Удалено: {total_before - total_after} записей (дубли, покрытые и смежные подсети)")


if __name__ == '__main__':
    main()
