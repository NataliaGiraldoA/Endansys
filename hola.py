from pathlib import Path
import shutil
import os


def restore_moved_images(dataset_path, backup_folder_name=None):
    """
    Restaura las imágenes que fueron movidas a la carpeta de archivos inválidos

    Args:
        dataset_path: Ruta original del dataset
        backup_folder_name: Nombre de la carpeta de backup (si es None, se detecta automáticamente)
    """
    dataset_path = Path(dataset_path)

    # Detectar carpeta de backup automáticamente si no se especifica
    if backup_folder_name is None:
        # Buscar carpetas que terminen en "_invalid_files"
        parent_dir = dataset_path.parent
        backup_candidates = [d for d in parent_dir.iterdir()
                             if d.is_dir() and d.name.endswith("_invalid_files")]

        if not backup_candidates:
            print("❌ No se encontró ninguna carpeta de archivos inválidos.")
            print("   Busca carpetas que terminen en '_invalid_files'")
            return False
        elif len(backup_candidates) > 1:
            print("⚠️  Se encontraron múltiples carpetas de backup:")
            for i, folder in enumerate(backup_candidates):
                print(f"   {i + 1}. {folder}")

            choice = input("Selecciona el número de la carpeta a restaurar (o 'q' para salir): ")
            if choice.lower() == 'q':
                return False

            try:
                choice_idx = int(choice) - 1
                backup_folder = backup_candidates[choice_idx]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                return False
        else:
            backup_folder = backup_candidates[0]
    else:
        backup_folder = dataset_path.parent / backup_folder_name

    if not backup_folder.exists():
        print(f"❌ La carpeta de backup no exists: {backup_folder}")
        return False

    print(f"📁 Restaurando archivos desde: {backup_folder}")
    print(f"📁 Destino: {dataset_path}")
    print("-" * 60)

    # Contar archivos a restaurar
    files_to_restore = list(backup_folder.rglob("*.*"))
    files_to_restore = [f for f in files_to_restore if f.is_file()]

    if not files_to_restore:
        print("ℹ️  No hay archivos para restaurar en la carpeta de backup.")
        return True

    print(f"Se encontraron {len(files_to_restore)} archivos para restaurar.")

    # Confirmar antes de proceder
    confirm = input("¿Deseas continuar con la restauración? (s/n): ").lower().strip()
    if confirm not in ['s', 'si', 'y', 'yes']:
        print("Operación cancelada.")
        return False

    restored_count = 0
    errors = []

    for file_path in files_to_restore:
        try:
            # Calcular la ruta original manteniendo la estructura
            relative_path = file_path.relative_to(backup_folder)
            original_path = dataset_path / relative_path

            # Crear carpetas padre si no existen
            original_path.parent.mkdir(parents=True, exist_ok=True)

            # Verificar si ya existe un archivo en el destino
            if original_path.exists():
                print(f"⚠️  Ya existe: {relative_path}")
                overwrite = input(f"   ¿Sobrescribir? (s/n/t=todos/q=quit): ").lower().strip()

                if overwrite == 'q':
                    break
                elif overwrite == 't':
                    # Sobrescribir este y todos los siguientes sin preguntar
                    shutil.move(str(file_path), str(original_path))
                    restored_count += 1
                    print(f"✅ Restaurado (sobrescrito): {relative_path}")
                    # Cambiar comportamiento para archivos siguientes
                    for remaining_file in files_to_restore[files_to_restore.index(file_path) + 1:]:
                        try:
                            remaining_relative = remaining_file.relative_to(backup_folder)
                            remaining_original = dataset_path / remaining_relative
                            remaining_original.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(remaining_file), str(remaining_original))
                            restored_count += 1
                            print(f"✅ Restaurado: {remaining_relative}")
                        except Exception as e:
                            errors.append((remaining_file, str(e)))
                    break
                elif overwrite in ['s', 'si', 'y', 'yes']:
                    shutil.move(str(file_path), str(original_path))
                    restored_count += 1
                    print(f"✅ Restaurado (sobrescrito): {relative_path}")
                else:
                    print(f"⏭️  Omitido: {relative_path}")
                    continue
            else:
                # Mover archivo a ubicación original
                shutil.move(str(file_path), str(original_path))
                restored_count += 1
                print(f"✅ Restaurado: {relative_path}")

        except Exception as e:
            error_msg = f"Error restaurando {file_path}: {str(e)}"
            errors.append((file_path, error_msg))
            print(f"❌ {error_msg}")

    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN DE RESTAURACIÓN:")
    print(f"   Archivos restaurados exitosamente: {restored_count}")
    print(f"   Errores: {len(errors)}")

    if errors:
        print(f"\n❌ ERRORES DURANTE LA RESTAURACIÓN:")
        for file_path, error in errors:
            print(f"   {file_path} -> {error}")

    # Preguntar si eliminar carpeta de backup vacía
    remaining_files = list(backup_folder.rglob("*.*"))
    remaining_files = [f for f in remaining_files if f.is_file()]

    if not remaining_files:
        delete_backup = input(f"\n🗑️  La carpeta de backup está vacía. ¿Eliminarla? (s/n): ").lower().strip()
        if delete_backup in ['s', 'si', 'y', 'yes']:
            try:
                shutil.rmtree(backup_folder)
                print(f"✅ Carpeta de backup eliminada: {backup_folder}")
            except Exception as e:
                print(f"❌ Error eliminando carpeta de backup: {e}")

    print(f"\n✅ Restauración completada!")
    return True


def list_backup_folders(dataset_path):
    """Lista todas las carpetas de backup disponibles"""
    dataset_path = Path(dataset_path)
    parent_dir = dataset_path.parent

    backup_folders = [d for d in parent_dir.iterdir()
                      if d.is_dir() and d.name.endswith("_invalid_files")]

    if backup_folders:
        print("📁 Carpetas de backup encontradas:")
        for folder in backup_folders:
            file_count = len([f for f in folder.rglob("*.*") if f.is_file()])
            print(f"   {folder.name} ({file_count} archivos)")
    else:
        print("ℹ️  No se encontraron carpetas de backup.")

    return backup_folders


# Ejemplo de uso
if __name__ == "__main__":
    # Cambia esta ruta por la tuya
    dataset_path = "C:/Users/Natalia/Desktop/PADIA/endansys/dataset/training"

    print("🔄 RESTAURADOR DE IMÁGENES MOVIDAS")
    print("=" * 50)

    # Mostrar carpetas de backup disponibles
    list_backup_folders(dataset_path)

    # Restaurar archivos
    success = restore_moved_images(dataset_path)

    if success:
        print("\n🎉 ¡Proceso de restauración completado!")
    else:
        print("\n❌ No se pudo completar la restauración.")