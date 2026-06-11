from editor.base.operation import EditOperation


class StreamOperation(EditOperation):
    """Marker base for operations that use stream copy (-c copy).

    Stream operations are always executed before filter operations so that
    structural edits (trim, cut) happen on the original stream without
    forcing a re-encode. The pipeline runs these sequentially via apply().

    Future: add input_args() / output_args() to let the pipeline compose
    multiple stream operations into a single ffmpeg subprocess.
    """
