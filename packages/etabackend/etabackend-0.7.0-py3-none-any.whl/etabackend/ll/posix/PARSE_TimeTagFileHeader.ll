; ModuleID = 'etabackend/cpp/PARSE_TimeTagFileHeader.cpp'
source_filename = "etabackend/cpp/PARSE_TimeTagFileHeader.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.TgHd = type { [32 x i8], i32, i32, i64 }
%struct.tm = type { i32, i32, i32, i32, i32, i32, i32, i32, i32, i64, i8* }

@order_gurantee = dso_local global i64 0, align 8
@SYNCRate_pspr = dso_local global i64 0, align 8
@TTRes_pspr = dso_local global i64 0, align 8
@DTRes_pspr = dso_local global i64 0, align 8
@NumRecords = dso_local global i64 0, align 8
@RecordType = dso_local global i64 0, align 8
@BytesofRecords = dso_local global i64 0, align 8
@TTF_header_offset = dso_local global i64 0, align 8
@.str = private unnamed_addr constant [64 x i8] c"\0ABecker & Hickl SPC-134/144/154/830 timetag file has no header.\00", align 1
@.str.1 = private unnamed_addr constant [27 x i8] c"\0ARecordType: bh_spc_4bytes\00", align 1
@.str.2 = private unnamed_addr constant [48 x i8] c"\0ASwebian Instrument timetag file has no header.\00", align 1
@.str.3 = private unnamed_addr constant [40 x i8] c"\0ARecordType: SwebianInstrument 16-bytes\00", align 1
@.str.4 = private unnamed_addr constant [45 x i8] c"\0A [ERROR]Error when reading header, aborted.\00", align 1
@.str.5 = private unnamed_addr constant [55 x i8] c"\0AquTAU_FORMAT_BINARY file header is read, but ignored.\00", align 1
@.str.6 = private unnamed_addr constant [42 x i8] c"\0ARecordType: quTAU_FORMAT_BINARY 10-bytes\00", align 1
@.str.7 = private unnamed_addr constant [59 x i8] c"\0AquTAU_FORMAT_COMPRESSED file header is read, but ignored.\00", align 1
@.str.8 = private unnamed_addr constant [45 x i8] c"\0ARecordType: quTAU_FORMAT_COMPRESSED 5-bytes\00", align 1
@TagHead = dso_local global %struct.TgHd zeroinitializer, align 8
@.str.9 = private unnamed_addr constant [41 x i8] c"\0A [ERROR]\0Aerror reading header, aborted.\00", align 1
@.str.10 = private unnamed_addr constant [23 x i8] c"\0APTU file Header: %s \0A\00", align 1
@.str.11 = private unnamed_addr constant [19 x i8] c"\0A\0AIncomplete File.\00", align 1
@.str.12 = private unnamed_addr constant [7 x i8] c"%s(%d)\00", align 1
@.str.13 = private unnamed_addr constant [7 x i8] c"\0A%-40s\00", align 1
@.str.14 = private unnamed_addr constant [12 x i8] c"<empty Tag>\00", align 1
@.str.15 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.16 = private unnamed_addr constant [5 x i8] c"True\00", align 1
@.str.17 = private unnamed_addr constant [6 x i8] c"False\00", align 1
@.str.18 = private unnamed_addr constant [5 x i8] c"%lld\00", align 1
@.str.19 = private unnamed_addr constant [25 x i8] c"TTResult_NumberOfRecords\00", align 1
@.str.20 = private unnamed_addr constant [27 x i8] c"TTResultFormat_TTTRRecType\00", align 1
@.str.21 = private unnamed_addr constant [10 x i8] c"0x%16.16X\00", align 1
@.str.22 = private unnamed_addr constant [3 x i8] c"%E\00", align 1
@.str.23 = private unnamed_addr constant [20 x i8] c"MeasDesc_Resolution\00", align 1
@.str.24 = private unnamed_addr constant [26 x i8] c"MeasDesc_GlobalResolution\00", align 1
@.str.25 = private unnamed_addr constant [30 x i8] c"<Float Array with %d Entries>\00", align 1
@.str.26 = private unnamed_addr constant [2 x i8] zeroinitializer, align 1
@.str.27 = private unnamed_addr constant [18 x i8] c"\0AIncomplete File.\00", align 1
@.str.28 = private unnamed_addr constant [3 x i32] [i32 37, i32 115, i32 0], align 4
@.str.29 = private unnamed_addr constant [32 x i8] c"<Binary Blob contains %d Bytes>\00", align 1
@.str.30 = private unnamed_addr constant [44 x i8] c"Illegal Type identifier found! Broken file?\00", align 1
@.str.31 = private unnamed_addr constant [11 x i8] c"Header_End\00", align 1
@.str.32 = private unnamed_addr constant [27 x i8] c"\0A\0A-----------------------\0A\00", align 1
@.str.33 = private unnamed_addr constant [19 x i8] c"\0APicoHarp T2 data\0A\00", align 1
@.str.34 = private unnamed_addr constant [23 x i8] c"\0AHydraHarp V1 T2 data\0A\00", align 1
@.str.35 = private unnamed_addr constant [23 x i8] c"\0AHydraHarp V2 T2 data\0A\00", align 1
@.str.36 = private unnamed_addr constant [23 x i8] c"\0ATimeHarp260N T2 data\0A\00", align 1
@.str.37 = private unnamed_addr constant [23 x i8] c"\0ATimeHarp260P T2 data\0A\00", align 1
@.str.38 = private unnamed_addr constant [19 x i8] c"\0APicoHarp T3 data\0A\00", align 1
@.str.39 = private unnamed_addr constant [23 x i8] c"\0AHydraHarp V1 T3 data\0A\00", align 1
@.str.40 = private unnamed_addr constant [23 x i8] c"\0AHydraHarp V2 T3 data\0A\00", align 1
@.str.41 = private unnamed_addr constant [23 x i8] c"\0ATimeHarp260N T3 data\0A\00", align 1
@.str.42 = private unnamed_addr constant [23 x i8] c"\0ATimeHarp260P T3 data\0A\00", align 1
@.str.43 = private unnamed_addr constant [44 x i8] c"\0AUnknown time-tag record type: 0x%X\0A 0x%X\0A \00", align 1
@.str.44 = private unnamed_addr constant [41 x i8] c"\0A [ERROR]Failed to read header, aborted.\00", align 1
@.str.45 = private unnamed_addr constant [7 x i8] c"PQTTTR\00", align 1
@.str.46 = private unnamed_addr constant [5 x i8] c"\87\B3\91\FA\00", align 1
@.str.47 = private unnamed_addr constant [38 x i8] c"\0AHeader Parser: quTAU_FORMAT_BINARY \0A\00", align 1
@.str.48 = private unnamed_addr constant [37 x i8] c"\0AHeader Parser: Swebian Instrument \0A\00", align 1
@.str.49 = private unnamed_addr constant [42 x i8] c"\0AHeader Parser: quTAU_FORMAT_COMPRESSED \0A\00", align 1
@.str.50 = private unnamed_addr constant [32 x i8] c"\0AHeader Parser: bh_spc_4bytes \0A\00", align 1
@.str.51 = private unnamed_addr constant [28 x i8] c"\0AHeader Parser: PicoQuant \0A\00", align 1
@.str.52 = private unnamed_addr constant [95 x i8] c"\0A [ERROR]Unidentified time-tag format. Specify one the with eta.run(...format=???). Aborted. \0A\00", align 1
@.str.53 = private unnamed_addr constant [20 x i8] c"\0ANumRecords: %lld \0A\00", align 1

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i64 @_Z5breadPvmmPc(i8*, i64, i64, i8*) #0 {
  %5 = alloca i8*, align 8
  %6 = alloca i64, align 8
  %7 = alloca i64, align 8
  %8 = alloca i8*, align 8
  store i8* %0, i8** %5, align 8
  store i64 %1, i64* %6, align 8
  store i64 %2, i64* %7, align 8
  store i8* %3, i8** %8, align 8
  %9 = load i8*, i8** %5, align 8
  %10 = load i8*, i8** %8, align 8
  %11 = load i64, i64* @TTF_header_offset, align 8
  %12 = getelementptr inbounds i8, i8* %10, i64 %11
  %13 = load i64, i64* %6, align 8
  %14 = load i64, i64* %7, align 8
  %15 = mul i64 %13, %14
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %9, i8* align 1 %12, i64 %15, i1 false)
  %16 = load i64, i64* %6, align 8
  %17 = load i64, i64* %7, align 8
  %18 = mul i64 %16, %17
  %19 = load i64, i64* @TTF_header_offset, align 8
  %20 = add i64 %19, %18
  store i64 %20, i64* @TTF_header_offset, align 8
  %21 = load i64, i64* %6, align 8
  %22 = load i64, i64* %7, align 8
  %23 = mul i64 %21, %22
  ret i64 %23
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i1) #1

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z23bh_4bytes_header_parserPc(i8*) #2 {
  %2 = alloca i8*, align 8
  store i8* %0, i8** %2, align 8
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @.str, i32 0, i32 0))
  %4 = sext i32 %3 to i64
  store i64 %4, i64* @order_gurantee, align 8
  %5 = load i8*, i8** %2, align 8
  %6 = bitcast i8* %5 to i16*
  %7 = getelementptr inbounds i16, i16* %6, i64 0
  %8 = load i16, i16* %7, align 2
  %9 = zext i16 %8 to i64
  store i64 %9, i64* @SYNCRate_pspr, align 8
  store i64 1, i64* @DTRes_pspr, align 8
  store i64 0, i64* @TTRes_pspr, align 8
  store i64 3, i64* @RecordType, align 8
  %10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.1, i32 0, i32 0))
  %11 = sext i32 %10 to i64
  store i64 %11, i64* @order_gurantee, align 8
  store i64 4, i64* @BytesofRecords, align 8
  store i64 4, i64* @TTF_header_offset, align 8
  ret i32 0
}

declare dso_local i32 @printf(i8*, ...) #3

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z21Swebian_header_parserv() #2 {
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @.str.2, i32 0, i32 0))
  %2 = sext i32 %1 to i64
  store i64 %2, i64* @order_gurantee, align 8
  store i64 0, i64* @SYNCRate_pspr, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  store i64 1, i64* @DTRes_pspr, align 8
  store i64 1, i64* @RecordType, align 8
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.3, i32 0, i32 0))
  %4 = sext i32 %3 to i64
  store i64 %4, i64* @order_gurantee, align 8
  store i64 16, i64* @BytesofRecords, align 8
  store i64 0, i64* @TTF_header_offset, align 8
  ret i32 0
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z33quTAU_FORMAT_BINARY_header_parserPc(i8*) #2 {
  %2 = alloca i8*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i8*, align 8
  %6 = alloca i32, align 4
  %7 = alloca i8*, align 8
  %8 = alloca [32 x i8], align 16
  store i8* %0, i8** %7, align 8
  %9 = bitcast [32 x i8]* %8 to i8*
  %10 = load i8*, i8** %7, align 8
  store i8* %9, i8** %2, align 8
  store i64 1, i64* %3, align 8
  store i64 32, i64* %4, align 8
  store i8* %10, i8** %5, align 8
  %11 = load i8*, i8** %2, align 8
  %12 = load i8*, i8** %5, align 8
  %13 = load i64, i64* @TTF_header_offset, align 8
  %14 = getelementptr inbounds i8, i8* %12, i64 %13
  %15 = load i64, i64* %3, align 8
  %16 = load i64, i64* %4, align 8
  %17 = mul i64 %15, %16
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %11, i8* align 1 %14, i64 %17, i1 false) #7
  %18 = load i64, i64* %3, align 8
  %19 = load i64, i64* %4, align 8
  %20 = mul i64 %18, %19
  %21 = load i64, i64* @TTF_header_offset, align 8
  %22 = add i64 %21, %20
  store i64 %22, i64* @TTF_header_offset, align 8
  %23 = load i64, i64* %3, align 8
  %24 = load i64, i64* %4, align 8
  %25 = mul i64 %23, %24
  %26 = icmp ne i64 %25, 32
  br i1 %26, label %27, label %30

; <label>:27:                                     ; preds = %1
  %28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.4, i32 0, i32 0))
  %29 = sext i32 %28 to i64
  store i64 %29, i64* @order_gurantee, align 8
  store i32 -1, i32* %6, align 4
  br label %36

; <label>:30:                                     ; preds = %1
  %31 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([55 x i8], [55 x i8]* @.str.5, i32 0, i32 0))
  %32 = sext i32 %31 to i64
  store i64 %32, i64* @order_gurantee, align 8
  store i64 0, i64* @RecordType, align 8
  store i64 10, i64* @BytesofRecords, align 8
  %33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([42 x i8], [42 x i8]* @.str.6, i32 0, i32 0))
  %34 = sext i32 %33 to i64
  store i64 %34, i64* @order_gurantee, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  %35 = load i64, i64* @TTRes_pspr, align 8
  store i64 %35, i64* @DTRes_pspr, align 8
  store i64 1249, i64* @SYNCRate_pspr, align 8
  store i32 0, i32* %6, align 4
  br label %36

; <label>:36:                                     ; preds = %30, %27
  %37 = load i32, i32* %6, align 4
  ret i32 %37
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z37quTAU_FORMAT_COMPRESSED_header_parserPc(i8*) #2 {
  %2 = alloca i8*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i8*, align 8
  %6 = alloca i32, align 4
  %7 = alloca i8*, align 8
  %8 = alloca [32 x i8], align 16
  store i8* %0, i8** %7, align 8
  %9 = bitcast [32 x i8]* %8 to i8*
  %10 = load i8*, i8** %7, align 8
  store i8* %9, i8** %2, align 8
  store i64 1, i64* %3, align 8
  store i64 32, i64* %4, align 8
  store i8* %10, i8** %5, align 8
  %11 = load i8*, i8** %2, align 8
  %12 = load i8*, i8** %5, align 8
  %13 = load i64, i64* @TTF_header_offset, align 8
  %14 = getelementptr inbounds i8, i8* %12, i64 %13
  %15 = load i64, i64* %3, align 8
  %16 = load i64, i64* %4, align 8
  %17 = mul i64 %15, %16
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %11, i8* align 1 %14, i64 %17, i1 false) #7
  %18 = load i64, i64* %3, align 8
  %19 = load i64, i64* %4, align 8
  %20 = mul i64 %18, %19
  %21 = load i64, i64* @TTF_header_offset, align 8
  %22 = add i64 %21, %20
  store i64 %22, i64* @TTF_header_offset, align 8
  %23 = load i64, i64* %3, align 8
  %24 = load i64, i64* %4, align 8
  %25 = mul i64 %23, %24
  %26 = icmp ne i64 %25, 32
  br i1 %26, label %27, label %30

; <label>:27:                                     ; preds = %1
  %28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.4, i32 0, i32 0))
  %29 = sext i32 %28 to i64
  store i64 %29, i64* @order_gurantee, align 8
  store i32 -1, i32* %6, align 4
  br label %36

; <label>:30:                                     ; preds = %1
  %31 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([59 x i8], [59 x i8]* @.str.7, i32 0, i32 0))
  %32 = sext i32 %31 to i64
  store i64 %32, i64* @order_gurantee, align 8
  store i64 0, i64* @RecordType, align 8
  store i64 5, i64* @BytesofRecords, align 8
  %33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.8, i32 0, i32 0))
  %34 = sext i32 %33 to i64
  store i64 %34, i64* @order_gurantee, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  %35 = load i64, i64* @TTRes_pspr, align 8
  store i64 %35, i64* @DTRes_pspr, align 8
  store i64 1249, i64* @SYNCRate_pspr, align 8
  store i32 0, i32* %6, align 4
  br label %36

; <label>:36:                                     ; preds = %30, %27
  %37 = load i32, i32* %6, align 4
  ret i32 %37
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i64 @_Z15TDateTime_TimeTd(double) #4 {
  %2 = alloca double, align 8
  %3 = alloca i64, align 8
  store double %0, double* %2, align 8
  %4 = load double, double* %2, align 8
  %5 = fsub double %4, 2.556900e+04
  %6 = fmul double %5, 8.640000e+04
  %7 = fptosi double %6 to i64
  store i64 %7, i64* %3, align 8
  %8 = load i64, i64* %3, align 8
  ret i64 %8
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z23PicoQuant_header_parserPc(i8*) #2 {
  %2 = alloca i8*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i8*, align 8
  %6 = alloca i8*, align 8
  %7 = alloca i64, align 8
  %8 = alloca i64, align 8
  %9 = alloca i8*, align 8
  %10 = alloca i8*, align 8
  %11 = alloca i64, align 8
  %12 = alloca i64, align 8
  %13 = alloca i8*, align 8
  %14 = alloca i8*, align 8
  %15 = alloca i64, align 8
  %16 = alloca i64, align 8
  %17 = alloca i8*, align 8
  %18 = alloca i32, align 4
  %19 = alloca i8*, align 8
  %20 = alloca i32, align 4
  %21 = alloca i8*, align 8
  %22 = alloca i32*, align 8
  %23 = alloca [8 x i8], align 1
  %24 = alloca [40 x i8], align 16
  %25 = alloca double, align 8
  %26 = alloca double, align 8
  %27 = alloca i64, align 8
  %28 = alloca i8, align 1
  store i8* %0, i8** %19, align 8
  %29 = bitcast [8 x i8]* %23 to i8*
  %30 = load i8*, i8** %19, align 8
  store i8* %29, i8** %14, align 8
  store i64 1, i64* %15, align 8
  store i64 8, i64* %16, align 8
  store i8* %30, i8** %17, align 8
  %31 = load i8*, i8** %14, align 8
  %32 = load i8*, i8** %17, align 8
  %33 = load i64, i64* @TTF_header_offset, align 8
  %34 = getelementptr inbounds i8, i8* %32, i64 %33
  %35 = load i64, i64* %15, align 8
  %36 = load i64, i64* %16, align 8
  %37 = mul i64 %35, %36
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %31, i8* align 1 %34, i64 %37, i1 false) #7
  %38 = load i64, i64* %15, align 8
  %39 = load i64, i64* %16, align 8
  %40 = mul i64 %38, %39
  %41 = load i64, i64* @TTF_header_offset, align 8
  %42 = add i64 %41, %40
  store i64 %42, i64* @TTF_header_offset, align 8
  %43 = load i64, i64* %15, align 8
  %44 = load i64, i64* %16, align 8
  %45 = mul i64 %43, %44
  %46 = trunc i64 %45 to i32
  store i32 %46, i32* %20, align 4
  %47 = load i32, i32* %20, align 4
  %48 = sext i32 %47 to i64
  %49 = icmp ne i64 %48, 8
  br i1 %49, label %50, label %53

; <label>:50:                                     ; preds = %1
  %51 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.9, i32 0, i32 0))
  %52 = sext i32 %51 to i64
  store i64 %52, i64* @order_gurantee, align 8
  br label %275

; <label>:53:                                     ; preds = %1
  %54 = getelementptr inbounds [8 x i8], [8 x i8]* %23, i32 0, i32 0
  %55 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.10, i32 0, i32 0), i8* %54)
  %56 = sext i32 %55 to i64
  store i64 %56, i64* @order_gurantee, align 8
  br label %57

; <label>:57:                                     ; preds = %227, %53
  %58 = load i8*, i8** %19, align 8
  store i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8** %2, align 8
  store i64 1, i64* %3, align 8
  store i64 48, i64* %4, align 8
  store i8* %58, i8** %5, align 8
  %59 = load i8*, i8** %2, align 8
  %60 = load i8*, i8** %5, align 8
  %61 = load i64, i64* @TTF_header_offset, align 8
  %62 = getelementptr inbounds i8, i8* %60, i64 %61
  %63 = load i64, i64* %3, align 8
  %64 = load i64, i64* %4, align 8
  %65 = mul i64 %63, %64
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %59, i8* align 1 %62, i64 %65, i1 false) #7
  %66 = load i64, i64* %3, align 8
  %67 = load i64, i64* %4, align 8
  %68 = mul i64 %66, %67
  %69 = load i64, i64* @TTF_header_offset, align 8
  %70 = add i64 %69, %68
  store i64 %70, i64* @TTF_header_offset, align 8
  %71 = load i64, i64* %3, align 8
  %72 = load i64, i64* %4, align 8
  %73 = mul i64 %71, %72
  %74 = trunc i64 %73 to i32
  store i32 %74, i32* %20, align 4
  %75 = load i32, i32* %20, align 4
  %76 = sext i32 %75 to i64
  %77 = icmp ne i64 %76, 48
  br i1 %77, label %78, label %81

; <label>:78:                                     ; preds = %57
  %79 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.11, i32 0, i32 0))
  %80 = sext i32 %79 to i64
  store i64 %80, i64* @order_gurantee, align 8
  br label %275

; <label>:81:                                     ; preds = %57
  %82 = getelementptr inbounds [40 x i8], [40 x i8]* %24, i32 0, i32 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %82, i8* align 8 getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i64 40, i1 false)
  %83 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 1), align 8
  %84 = icmp sgt i32 %83, -1
  br i1 %84, label %85, label %89

; <label>:85:                                     ; preds = %81
  %86 = getelementptr inbounds [40 x i8], [40 x i8]* %24, i32 0, i32 0
  %87 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 1), align 8
  %88 = call i32 (i8*, i8*, ...) @sprintf(i8* %86, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.12, i32 0, i32 0), i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i32 %87) #7
  br label %89

; <label>:89:                                     ; preds = %85, %81
  %90 = getelementptr inbounds [40 x i8], [40 x i8]* %24, i32 0, i32 0
  %91 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.13, i32 0, i32 0), i8* %90)
  %92 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 2), align 4
  switch i32 %92, label %224 [
    i32 -65528, label %93
    i32 8, label %95
    i32 268435464, label %101
    i32 285212680, label %114
    i32 301989896, label %117
    i32 536870920, label %120
    i32 537001983, label %139
    i32 553648136, label %144
    i32 1073872895, label %150
    i32 1073938431, label %183
    i32 -1, label %220
  ]

; <label>:93:                                     ; preds = %89
  %94 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str.14, i32 0, i32 0))
  br label %226

; <label>:95:                                     ; preds = %89
  %96 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %97 = icmp ne i64 %96, 0
  %98 = zext i1 %97 to i64
  %99 = select i1 %97, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.16, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.17, i32 0, i32 0)
  %100 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %99)
  br label %226

; <label>:101:                                    ; preds = %89
  %102 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %103 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.18, i32 0, i32 0), i64 %102)
  %104 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.str.19, i32 0, i32 0)) #8
  %105 = icmp eq i32 %104, 0
  br i1 %105, label %106, label %108

; <label>:106:                                    ; preds = %101
  %107 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %107, i64* @NumRecords, align 8
  br label %108

; <label>:108:                                    ; preds = %106, %101
  %109 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.20, i32 0, i32 0)) #8
  %110 = icmp eq i32 %109, 0
  br i1 %110, label %111, label %113

; <label>:111:                                    ; preds = %108
  %112 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %112, i64* @RecordType, align 8
  br label %113

; <label>:113:                                    ; preds = %111, %108
  br label %226

; <label>:114:                                    ; preds = %89
  %115 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %116 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.21, i32 0, i32 0), i64 %115)
  br label %226

; <label>:117:                                    ; preds = %89
  %118 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %119 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.21, i32 0, i32 0), i64 %118)
  br label %226

; <label>:120:                                    ; preds = %89
  %121 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  %122 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.22, i32 0, i32 0), double %121)
  %123 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.str.23, i32 0, i32 0)) #8
  %124 = icmp eq i32 %123, 0
  br i1 %124, label %125, label %130

; <label>:125:                                    ; preds = %120
  %126 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  store double %126, double* %25, align 8
  %127 = load double, double* %25, align 8
  %128 = fmul double %127, 1.000000e+12
  %129 = fptosi double %128 to i64
  store i64 %129, i64* @DTRes_pspr, align 8
  br label %130

; <label>:130:                                    ; preds = %125, %120
  %131 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.24, i32 0, i32 0)) #8
  %132 = icmp eq i32 %131, 0
  br i1 %132, label %133, label %138

; <label>:133:                                    ; preds = %130
  %134 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  store double %134, double* %26, align 8
  %135 = load double, double* %26, align 8
  %136 = fmul double %135, 1.000000e+12
  %137 = fptosi double %136 to i64
  store i64 %137, i64* @TTRes_pspr, align 8
  br label %138

; <label>:138:                                    ; preds = %133, %130
  br label %226

; <label>:139:                                    ; preds = %89
  %140 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %141 = udiv i64 %140, 8
  %142 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str.25, i32 0, i32 0), i64 %141)
  %143 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %143, i64* @TTF_header_offset, align 8
  br label %226

; <label>:144:                                    ; preds = %89
  %145 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  %146 = call i64 @_Z15TDateTime_TimeTd(double %145)
  store i64 %146, i64* %27, align 8
  %147 = call %struct.tm* @gmtime(i64* %27) #7
  %148 = call i8* @asctime(%struct.tm* %147) #7
  %149 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %148, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.26, i32 0, i32 0))
  br label %226

; <label>:150:                                    ; preds = %89
  %151 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %152 = call noalias i8* @calloc(i64 %151, i64 1) #7
  store i8* %152, i8** %21, align 8
  %153 = load i8*, i8** %21, align 8
  %154 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %155 = load i8*, i8** %19, align 8
  store i8* %153, i8** %6, align 8
  store i64 1, i64* %7, align 8
  store i64 %154, i64* %8, align 8
  store i8* %155, i8** %9, align 8
  %156 = load i8*, i8** %6, align 8
  %157 = load i8*, i8** %9, align 8
  %158 = load i64, i64* @TTF_header_offset, align 8
  %159 = getelementptr inbounds i8, i8* %157, i64 %158
  %160 = load i64, i64* %7, align 8
  %161 = load i64, i64* %8, align 8
  %162 = mul i64 %160, %161
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %156, i8* align 1 %159, i64 %162, i1 false) #7
  %163 = load i64, i64* %7, align 8
  %164 = load i64, i64* %8, align 8
  %165 = mul i64 %163, %164
  %166 = load i64, i64* @TTF_header_offset, align 8
  %167 = add i64 %166, %165
  store i64 %167, i64* @TTF_header_offset, align 8
  %168 = load i64, i64* %7, align 8
  %169 = load i64, i64* %8, align 8
  %170 = mul i64 %168, %169
  %171 = trunc i64 %170 to i32
  store i32 %171, i32* %20, align 4
  %172 = load i32, i32* %20, align 4
  %173 = sext i32 %172 to i64
  %174 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %175 = icmp ne i64 %173, %174
  br i1 %175, label %176, label %179

; <label>:176:                                    ; preds = %150
  %177 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.27, i32 0, i32 0))
  %178 = load i8*, i8** %21, align 8
  call void @free(i8* %178) #7
  br label %275

; <label>:179:                                    ; preds = %150
  %180 = load i8*, i8** %21, align 8
  %181 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %180)
  %182 = load i8*, i8** %21, align 8
  call void @free(i8* %182) #7
  br label %226

; <label>:183:                                    ; preds = %89
  %184 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %185 = call noalias i8* @calloc(i64 %184, i64 1) #7
  %186 = bitcast i8* %185 to i32*
  store i32* %186, i32** %22, align 8
  %187 = load i32*, i32** %22, align 8
  %188 = bitcast i32* %187 to i8*
  %189 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %190 = load i8*, i8** %19, align 8
  store i8* %188, i8** %10, align 8
  store i64 1, i64* %11, align 8
  store i64 %189, i64* %12, align 8
  store i8* %190, i8** %13, align 8
  %191 = load i8*, i8** %10, align 8
  %192 = load i8*, i8** %13, align 8
  %193 = load i64, i64* @TTF_header_offset, align 8
  %194 = getelementptr inbounds i8, i8* %192, i64 %193
  %195 = load i64, i64* %11, align 8
  %196 = load i64, i64* %12, align 8
  %197 = mul i64 %195, %196
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %191, i8* align 1 %194, i64 %197, i1 false) #7
  %198 = load i64, i64* %11, align 8
  %199 = load i64, i64* %12, align 8
  %200 = mul i64 %198, %199
  %201 = load i64, i64* @TTF_header_offset, align 8
  %202 = add i64 %201, %200
  store i64 %202, i64* @TTF_header_offset, align 8
  %203 = load i64, i64* %11, align 8
  %204 = load i64, i64* %12, align 8
  %205 = mul i64 %203, %204
  %206 = trunc i64 %205 to i32
  store i32 %206, i32* %20, align 4
  %207 = load i32, i32* %20, align 4
  %208 = sext i32 %207 to i64
  %209 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %210 = icmp ne i64 %208, %209
  br i1 %210, label %211, label %215

; <label>:211:                                    ; preds = %183
  %212 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.27, i32 0, i32 0))
  %213 = load i32*, i32** %22, align 8
  %214 = bitcast i32* %213 to i8*
  call void @free(i8* %214) #7
  br label %275

; <label>:215:                                    ; preds = %183
  %216 = load i32*, i32** %22, align 8
  %217 = call i32 (i32*, ...) @wprintf(i32* getelementptr inbounds ([3 x i32], [3 x i32]* @.str.28, i32 0, i32 0), i32* %216)
  %218 = load i32*, i32** %22, align 8
  %219 = bitcast i32* %218 to i8*
  call void @free(i8* %219) #7
  br label %226

; <label>:220:                                    ; preds = %89
  %221 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %222 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([32 x i8], [32 x i8]* @.str.29, i32 0, i32 0), i64 %221)
  %223 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %223, i64* @TTF_header_offset, align 8
  br label %226

; <label>:224:                                    ; preds = %89
  %225 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str.30, i32 0, i32 0))
  br label %275

; <label>:226:                                    ; preds = %220, %215, %179, %144, %139, %138, %117, %114, %113, %95, %93
  br label %227

; <label>:227:                                    ; preds = %226
  %228 = call i32 @strncmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.31, i32 0, i32 0), i64 11) #8
  %229 = icmp ne i32 %228, 0
  br i1 %229, label %57, label %230

; <label>:230:                                    ; preds = %227
  %231 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.32, i32 0, i32 0))
  %232 = sext i32 %231 to i64
  store i64 %232, i64* @order_gurantee, align 8
  %233 = load i64, i64* @RecordType, align 8
  switch i64 %233, label %264 [
    i64 66051, label %234
    i64 66052, label %237
    i64 16843268, label %240
    i64 66053, label %243
    i64 66054, label %246
    i64 66307, label %249
    i64 66308, label %252
    i64 16843524, label %255
    i64 66309, label %258
    i64 66310, label %261
  ]

; <label>:234:                                    ; preds = %230
  %235 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.33, i32 0, i32 0))
  %236 = sext i32 %235 to i64
  store i64 %236, i64* @order_gurantee, align 8
  store i8 1, i8* %28, align 1
  br label %268

; <label>:237:                                    ; preds = %230
  %238 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.34, i32 0, i32 0))
  %239 = sext i32 %238 to i64
  store i64 %239, i64* @order_gurantee, align 8
  store i8 1, i8* %28, align 1
  br label %268

; <label>:240:                                    ; preds = %230
  %241 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.35, i32 0, i32 0))
  %242 = sext i32 %241 to i64
  store i64 %242, i64* @order_gurantee, align 8
  store i8 1, i8* %28, align 1
  br label %268

; <label>:243:                                    ; preds = %230
  %244 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.36, i32 0, i32 0))
  %245 = sext i32 %244 to i64
  store i64 %245, i64* @order_gurantee, align 8
  store i8 1, i8* %28, align 1
  br label %268

; <label>:246:                                    ; preds = %230
  %247 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.37, i32 0, i32 0))
  %248 = sext i32 %247 to i64
  store i64 %248, i64* @order_gurantee, align 8
  store i8 1, i8* %28, align 1
  br label %268

; <label>:249:                                    ; preds = %230
  %250 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.38, i32 0, i32 0))
  %251 = sext i32 %250 to i64
  store i64 %251, i64* @order_gurantee, align 8
  store i8 0, i8* %28, align 1
  br label %268

; <label>:252:                                    ; preds = %230
  %253 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.39, i32 0, i32 0))
  %254 = sext i32 %253 to i64
  store i64 %254, i64* @order_gurantee, align 8
  store i8 0, i8* %28, align 1
  br label %268

; <label>:255:                                    ; preds = %230
  %256 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.40, i32 0, i32 0))
  %257 = sext i32 %256 to i64
  store i64 %257, i64* @order_gurantee, align 8
  store i8 0, i8* %28, align 1
  br label %268

; <label>:258:                                    ; preds = %230
  %259 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.41, i32 0, i32 0))
  %260 = sext i32 %259 to i64
  store i64 %260, i64* @order_gurantee, align 8
  store i8 0, i8* %28, align 1
  br label %268

; <label>:261:                                    ; preds = %230
  %262 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.42, i32 0, i32 0))
  %263 = sext i32 %262 to i64
  store i64 %263, i64* @order_gurantee, align 8
  store i8 0, i8* %28, align 1
  br label %268

; <label>:264:                                    ; preds = %230
  %265 = load i64, i64* @RecordType, align 8
  %266 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str.43, i32 0, i32 0), i64 %265)
  %267 = sext i32 %266 to i64
  store i64 %267, i64* @order_gurantee, align 8
  br label %275

; <label>:268:                                    ; preds = %261, %258, %255, %252, %249, %246, %243, %240, %237, %234
  %269 = load i8, i8* %28, align 1
  %270 = trunc i8 %269 to i1
  br i1 %270, label %271, label %272

; <label>:271:                                    ; preds = %268
  store i64 12495, i64* @SYNCRate_pspr, align 8
  br label %274

; <label>:272:                                    ; preds = %268
  %273 = load i64, i64* @TTRes_pspr, align 8
  store i64 %273, i64* @SYNCRate_pspr, align 8
  br label %274

; <label>:274:                                    ; preds = %272, %271
  store i64 4, i64* @BytesofRecords, align 8
  store i32 0, i32* %18, align 4
  br label %277

; <label>:275:                                    ; preds = %264, %224, %211, %176, %78, %50
  store i32 -1, i32* %18, align 4
  br label %277
                                                  ; No predecessors!
  store i32 -2, i32* %18, align 4
  br label %277

; <label>:277:                                    ; preds = %276, %275, %274
  %278 = load i32, i32* %18, align 4
  ret i32 %278
}

; Function Attrs: nounwind
declare dso_local i32 @sprintf(i8*, i8*, ...) #5

; Function Attrs: nounwind readonly
declare dso_local i32 @strcmp(i8*, i8*) #6

; Function Attrs: nounwind
declare dso_local i8* @asctime(%struct.tm*) #5

; Function Attrs: nounwind
declare dso_local %struct.tm* @gmtime(i64*) #5

; Function Attrs: nounwind
declare dso_local noalias i8* @calloc(i64, i64) #5

; Function Attrs: nounwind
declare dso_local void @free(i8*) #5

declare dso_local i32 @wprintf(i32*, ...) #3

; Function Attrs: nounwind readonly
declare dso_local i32 @strncmp(i8*, i8*, i64) #6

; Function Attrs: alwaysinline uwtable
define dso_local i32 @PARSE_TimeTagFileHeader(i8*, i32) #2 {
  %3 = alloca i8*, align 8
  %4 = alloca i8*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i8*, align 8
  %8 = alloca i32, align 4
  %9 = alloca i8*, align 8
  %10 = alloca i8*, align 8
  %11 = alloca i64, align 8
  %12 = alloca i64, align 8
  %13 = alloca i8*, align 8
  %14 = alloca i32, align 4
  %15 = alloca i8*, align 8
  %16 = alloca [32 x i8], align 16
  %17 = alloca i8*, align 8
  %18 = alloca i64, align 8
  %19 = alloca i64, align 8
  %20 = alloca i8*, align 8
  %21 = alloca i8*, align 8
  %22 = alloca i64, align 8
  %23 = alloca i64, align 8
  %24 = alloca i8*, align 8
  %25 = alloca i8*, align 8
  %26 = alloca i64, align 8
  %27 = alloca i64, align 8
  %28 = alloca i8*, align 8
  %29 = alloca i8*, align 8
  %30 = alloca i64, align 8
  %31 = alloca i64, align 8
  %32 = alloca i8*, align 8
  %33 = alloca i32, align 4
  %34 = alloca i8*, align 8
  %35 = alloca i32, align 4
  %36 = alloca i8*, align 8
  %37 = alloca i32*, align 8
  %38 = alloca [8 x i8], align 1
  %39 = alloca [40 x i8], align 16
  %40 = alloca double, align 8
  %41 = alloca double, align 8
  %42 = alloca i64, align 8
  %43 = alloca i8, align 1
  %44 = alloca i8*, align 8
  %45 = alloca i64, align 8
  %46 = alloca i64, align 8
  %47 = alloca i8*, align 8
  %48 = alloca i32, align 4
  %49 = alloca i8*, align 8
  %50 = alloca i32, align 4
  %51 = alloca i32, align 4
  %52 = alloca [8 x i8], align 1
  %53 = alloca i8, align 1
  store i8* %0, i8** %49, align 8
  store i32 %1, i32* %50, align 4
  store i32 -1, i32* %51, align 4
  store i64 0, i64* @TTF_header_offset, align 8
  %54 = bitcast [8 x i8]* %52 to i8*
  %55 = load i8*, i8** %49, align 8
  store i8* %54, i8** %44, align 8
  store i64 1, i64* %45, align 8
  store i64 8, i64* %46, align 8
  store i8* %55, i8** %47, align 8
  %56 = load i8*, i8** %44, align 8
  %57 = load i8*, i8** %47, align 8
  %58 = load i64, i64* @TTF_header_offset, align 8
  %59 = getelementptr inbounds i8, i8* %57, i64 %58
  %60 = load i64, i64* %45, align 8
  %61 = load i64, i64* %46, align 8
  %62 = mul i64 %60, %61
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %56, i8* align 1 %59, i64 %62, i1 false) #7
  %63 = load i64, i64* %45, align 8
  %64 = load i64, i64* %46, align 8
  %65 = mul i64 %63, %64
  %66 = load i64, i64* @TTF_header_offset, align 8
  %67 = add i64 %66, %65
  store i64 %67, i64* @TTF_header_offset, align 8
  %68 = load i64, i64* %45, align 8
  %69 = load i64, i64* %46, align 8
  %70 = mul i64 %68, %69
  %71 = icmp ne i64 %70, 8
  br i1 %71, label %72, label %75

; <label>:72:                                     ; preds = %2
  %73 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.44, i32 0, i32 0))
  %74 = sext i32 %73 to i64
  store i64 %74, i64* @order_gurantee, align 8
  store i32 -2, i32* %48, align 4
  br label %436

; <label>:75:                                     ; preds = %2
  store i8 1, i8* %53, align 1
  %76 = load i32, i32* %50, align 4
  %77 = icmp eq i32 %76, -1
  br i1 %77, label %78, label %89

; <label>:78:                                     ; preds = %75
  %79 = getelementptr inbounds [8 x i8], [8 x i8]* %52, i32 0, i32 0
  %80 = call i32 @strncmp(i8* %79, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.45, i32 0, i32 0), i64 6) #8
  %81 = icmp eq i32 %80, 0
  br i1 %81, label %82, label %83

; <label>:82:                                     ; preds = %78
  store i32 4, i32* %50, align 4
  br label %83

; <label>:83:                                     ; preds = %82, %78
  %84 = getelementptr inbounds [8 x i8], [8 x i8]* %52, i32 0, i32 0
  %85 = call i32 @strncmp(i8* %84, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.46, i32 0, i32 0), i64 4) #8
  %86 = icmp eq i32 %85, 0
  br i1 %86, label %87, label %88

; <label>:87:                                     ; preds = %83
  store i32 0, i32* %50, align 4
  br label %88

; <label>:88:                                     ; preds = %87, %83
  br label %89

; <label>:89:                                     ; preds = %88, %75
  %90 = load i32, i32* %50, align 4
  switch i32 %90, label %431 [
    i32 0, label %91
    i32 1, label %124
    i32 2, label %131
    i32 3, label %164
    i32 4, label %176
    i32 -1, label %428
  ]

; <label>:91:                                     ; preds = %89
  %92 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.47, i32 0, i32 0))
  %93 = sext i32 %92 to i64
  store i64 %93, i64* @order_gurantee, align 8
  %94 = load i8*, i8** %49, align 8
  store i8* %94, i8** %15, align 8
  %95 = bitcast [32 x i8]* %16 to i8*
  %96 = load i8*, i8** %15, align 8
  store i8* %95, i8** %10, align 8
  store i64 1, i64* %11, align 8
  store i64 32, i64* %12, align 8
  store i8* %96, i8** %13, align 8
  %97 = load i8*, i8** %10, align 8
  %98 = load i8*, i8** %13, align 8
  %99 = load i64, i64* @TTF_header_offset, align 8
  %100 = getelementptr inbounds i8, i8* %98, i64 %99
  %101 = load i64, i64* %11, align 8
  %102 = load i64, i64* %12, align 8
  %103 = mul i64 %101, %102
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %97, i8* align 1 %100, i64 %103, i1 false) #7
  %104 = load i64, i64* %11, align 8
  %105 = load i64, i64* %12, align 8
  %106 = mul i64 %104, %105
  %107 = load i64, i64* @TTF_header_offset, align 8
  %108 = add i64 %107, %106
  store i64 %108, i64* @TTF_header_offset, align 8
  %109 = load i64, i64* %11, align 8
  %110 = load i64, i64* %12, align 8
  %111 = mul i64 %109, %110
  %112 = icmp ne i64 %111, 32
  br i1 %112, label %113, label %116

; <label>:113:                                    ; preds = %91
  %114 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.4, i32 0, i32 0))
  %115 = sext i32 %114 to i64
  store i64 %115, i64* @order_gurantee, align 8
  store i32 -1, i32* %14, align 4
  br label %122

; <label>:116:                                    ; preds = %91
  %117 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([55 x i8], [55 x i8]* @.str.5, i32 0, i32 0))
  %118 = sext i32 %117 to i64
  store i64 %118, i64* @order_gurantee, align 8
  store i64 0, i64* @RecordType, align 8
  store i64 10, i64* @BytesofRecords, align 8
  %119 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([42 x i8], [42 x i8]* @.str.6, i32 0, i32 0))
  %120 = sext i32 %119 to i64
  store i64 %120, i64* @order_gurantee, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  %121 = load i64, i64* @TTRes_pspr, align 8
  store i64 %121, i64* @DTRes_pspr, align 8
  store i64 1249, i64* @SYNCRate_pspr, align 8
  store i32 0, i32* %14, align 4
  br label %122

; <label>:122:                                    ; preds = %113, %116
  %123 = load i32, i32* %14, align 4
  store i32 %123, i32* %51, align 4
  br label %431

; <label>:124:                                    ; preds = %89
  %125 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([37 x i8], [37 x i8]* @.str.48, i32 0, i32 0))
  %126 = sext i32 %125 to i64
  store i64 %126, i64* @order_gurantee, align 8
  %127 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @.str.2, i32 0, i32 0))
  %128 = sext i32 %127 to i64
  store i64 %128, i64* @order_gurantee, align 8
  store i64 0, i64* @SYNCRate_pspr, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  store i64 1, i64* @DTRes_pspr, align 8
  store i64 1, i64* @RecordType, align 8
  %129 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.3, i32 0, i32 0))
  %130 = sext i32 %129 to i64
  store i64 %130, i64* @order_gurantee, align 8
  store i64 16, i64* @BytesofRecords, align 8
  store i64 0, i64* @TTF_header_offset, align 8
  store i32 0, i32* %51, align 4
  br label %431

; <label>:131:                                    ; preds = %89
  %132 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([42 x i8], [42 x i8]* @.str.49, i32 0, i32 0))
  %133 = sext i32 %132 to i64
  store i64 %133, i64* @order_gurantee, align 8
  %134 = load i8*, i8** %49, align 8
  store i8* %134, i8** %9, align 8
  %135 = bitcast [32 x i8]* %16 to i8*
  %136 = load i8*, i8** %9, align 8
  store i8* %135, i8** %4, align 8
  store i64 1, i64* %5, align 8
  store i64 32, i64* %6, align 8
  store i8* %136, i8** %7, align 8
  %137 = load i8*, i8** %4, align 8
  %138 = load i8*, i8** %7, align 8
  %139 = load i64, i64* @TTF_header_offset, align 8
  %140 = getelementptr inbounds i8, i8* %138, i64 %139
  %141 = load i64, i64* %5, align 8
  %142 = load i64, i64* %6, align 8
  %143 = mul i64 %141, %142
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %137, i8* align 1 %140, i64 %143, i1 false) #7
  %144 = load i64, i64* %5, align 8
  %145 = load i64, i64* %6, align 8
  %146 = mul i64 %144, %145
  %147 = load i64, i64* @TTF_header_offset, align 8
  %148 = add i64 %147, %146
  store i64 %148, i64* @TTF_header_offset, align 8
  %149 = load i64, i64* %5, align 8
  %150 = load i64, i64* %6, align 8
  %151 = mul i64 %149, %150
  %152 = icmp ne i64 %151, 32
  br i1 %152, label %153, label %156

; <label>:153:                                    ; preds = %131
  %154 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.4, i32 0, i32 0))
  %155 = sext i32 %154 to i64
  store i64 %155, i64* @order_gurantee, align 8
  store i32 -1, i32* %8, align 4
  br label %162

; <label>:156:                                    ; preds = %131
  %157 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([59 x i8], [59 x i8]* @.str.7, i32 0, i32 0))
  %158 = sext i32 %157 to i64
  store i64 %158, i64* @order_gurantee, align 8
  store i64 0, i64* @RecordType, align 8
  store i64 5, i64* @BytesofRecords, align 8
  %159 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str.8, i32 0, i32 0))
  %160 = sext i32 %159 to i64
  store i64 %160, i64* @order_gurantee, align 8
  store i64 1, i64* @TTRes_pspr, align 8
  %161 = load i64, i64* @TTRes_pspr, align 8
  store i64 %161, i64* @DTRes_pspr, align 8
  store i64 1249, i64* @SYNCRate_pspr, align 8
  store i32 0, i32* %8, align 4
  br label %162

; <label>:162:                                    ; preds = %153, %156
  %163 = load i32, i32* %8, align 4
  store i32 %163, i32* %51, align 4
  br label %431

; <label>:164:                                    ; preds = %89
  %165 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([32 x i8], [32 x i8]* @.str.50, i32 0, i32 0))
  %166 = sext i32 %165 to i64
  store i64 %166, i64* @order_gurantee, align 8
  %167 = getelementptr inbounds [8 x i8], [8 x i8]* %52, i32 0, i32 0
  store i8* %167, i8** %3, align 8
  %168 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @.str, i32 0, i32 0))
  %169 = sext i32 %168 to i64
  store i64 %169, i64* @order_gurantee, align 8
  %170 = load i8*, i8** %3, align 8
  %171 = bitcast i8* %170 to i16*
  %172 = load i16, i16* %171, align 2
  %173 = zext i16 %172 to i64
  store i64 %173, i64* @SYNCRate_pspr, align 8
  store i64 1, i64* @DTRes_pspr, align 8
  store i64 0, i64* @TTRes_pspr, align 8
  store i64 3, i64* @RecordType, align 8
  %174 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.1, i32 0, i32 0))
  %175 = sext i32 %174 to i64
  store i64 %175, i64* @order_gurantee, align 8
  store i64 4, i64* @BytesofRecords, align 8
  store i64 4, i64* @TTF_header_offset, align 8
  store i32 0, i32* %51, align 4
  br label %431

; <label>:176:                                    ; preds = %89
  %177 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([28 x i8], [28 x i8]* @.str.51, i32 0, i32 0))
  %178 = sext i32 %177 to i64
  store i64 %178, i64* @order_gurantee, align 8
  %179 = load i8*, i8** %49, align 8
  store i8* %179, i8** %34, align 8
  %180 = bitcast [8 x i8]* %38 to i8*
  %181 = load i8*, i8** %34, align 8
  store i8* %180, i8** %29, align 8
  store i64 1, i64* %30, align 8
  store i64 8, i64* %31, align 8
  store i8* %181, i8** %32, align 8
  %182 = load i8*, i8** %29, align 8
  %183 = load i8*, i8** %32, align 8
  %184 = load i64, i64* @TTF_header_offset, align 8
  %185 = getelementptr inbounds i8, i8* %183, i64 %184
  %186 = load i64, i64* %30, align 8
  %187 = load i64, i64* %31, align 8
  %188 = mul i64 %186, %187
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %182, i8* align 1 %185, i64 %188, i1 false) #7
  %189 = load i64, i64* %30, align 8
  %190 = load i64, i64* %31, align 8
  %191 = mul i64 %189, %190
  %192 = load i64, i64* @TTF_header_offset, align 8
  %193 = add i64 %192, %191
  store i64 %193, i64* @TTF_header_offset, align 8
  %194 = load i64, i64* %30, align 8
  %195 = load i64, i64* %31, align 8
  %196 = mul i64 %194, %195
  %197 = trunc i64 %196 to i32
  store i32 %197, i32* %35, align 4
  %198 = load i32, i32* %35, align 4
  %199 = sext i32 %198 to i64
  %200 = icmp ne i64 %199, 8
  br i1 %200, label %201, label %204

; <label>:201:                                    ; preds = %176
  %202 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.9, i32 0, i32 0))
  %203 = sext i32 %202 to i64
  store i64 %203, i64* @order_gurantee, align 8
  br label %425

; <label>:204:                                    ; preds = %176
  %205 = getelementptr inbounds [8 x i8], [8 x i8]* %38, i32 0, i32 0
  %206 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.10, i32 0, i32 0), i8* %205)
  %207 = sext i32 %206 to i64
  store i64 %207, i64* @order_gurantee, align 8
  br label %208

; <label>:208:                                    ; preds = %377, %204
  %209 = load i8*, i8** %34, align 8
  store i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8** %17, align 8
  store i64 1, i64* %18, align 8
  store i64 48, i64* %19, align 8
  store i8* %209, i8** %20, align 8
  %210 = load i8*, i8** %17, align 8
  %211 = load i8*, i8** %20, align 8
  %212 = load i64, i64* @TTF_header_offset, align 8
  %213 = getelementptr inbounds i8, i8* %211, i64 %212
  %214 = load i64, i64* %18, align 8
  %215 = load i64, i64* %19, align 8
  %216 = mul i64 %214, %215
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %210, i8* align 1 %213, i64 %216, i1 false) #7
  %217 = load i64, i64* %18, align 8
  %218 = load i64, i64* %19, align 8
  %219 = mul i64 %217, %218
  %220 = load i64, i64* @TTF_header_offset, align 8
  %221 = add i64 %220, %219
  store i64 %221, i64* @TTF_header_offset, align 8
  %222 = load i64, i64* %18, align 8
  %223 = load i64, i64* %19, align 8
  %224 = mul i64 %222, %223
  %225 = trunc i64 %224 to i32
  store i32 %225, i32* %35, align 4
  %226 = load i32, i32* %35, align 4
  %227 = sext i32 %226 to i64
  %228 = icmp ne i64 %227, 48
  br i1 %228, label %229, label %232

; <label>:229:                                    ; preds = %208
  %230 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.11, i32 0, i32 0))
  %231 = sext i32 %230 to i64
  store i64 %231, i64* @order_gurantee, align 8
  br label %425

; <label>:232:                                    ; preds = %208
  %233 = getelementptr inbounds [40 x i8], [40 x i8]* %39, i32 0, i32 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %233, i8* align 8 getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i64 40, i1 false)
  %234 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 1), align 8
  %235 = icmp sgt i32 %234, -1
  br i1 %235, label %236, label %240

; <label>:236:                                    ; preds = %232
  %237 = getelementptr inbounds [40 x i8], [40 x i8]* %39, i32 0, i32 0
  %238 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 1), align 8
  %239 = call i32 (i8*, i8*, ...) @sprintf(i8* %237, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.12, i32 0, i32 0), i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i32 %238) #7
  br label %240

; <label>:240:                                    ; preds = %236, %232
  %241 = getelementptr inbounds [40 x i8], [40 x i8]* %39, i32 0, i32 0
  %242 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.13, i32 0, i32 0), i8* %241)
  %243 = load i32, i32* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 2), align 4
  switch i32 %243, label %375 [
    i32 -65528, label %244
    i32 8, label %246
    i32 268435464, label %252
    i32 285212680, label %265
    i32 301989896, label %268
    i32 536870920, label %271
    i32 537001983, label %290
    i32 553648136, label %295
    i32 1073872895, label %301
    i32 1073938431, label %334
    i32 -1, label %371
  ]

; <label>:244:                                    ; preds = %240
  %245 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str.14, i32 0, i32 0))
  br label %377

; <label>:246:                                    ; preds = %240
  %247 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %248 = icmp ne i64 %247, 0
  %249 = zext i1 %248 to i64
  %250 = select i1 %248, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.16, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.17, i32 0, i32 0)
  %251 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %250)
  br label %377

; <label>:252:                                    ; preds = %240
  %253 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %254 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.18, i32 0, i32 0), i64 %253)
  %255 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.str.19, i32 0, i32 0)) #8
  %256 = icmp eq i32 %255, 0
  br i1 %256, label %257, label %259

; <label>:257:                                    ; preds = %252
  %258 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %258, i64* @NumRecords, align 8
  br label %259

; <label>:259:                                    ; preds = %257, %252
  %260 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.20, i32 0, i32 0)) #8
  %261 = icmp eq i32 %260, 0
  br i1 %261, label %262, label %264

; <label>:262:                                    ; preds = %259
  %263 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %263, i64* @RecordType, align 8
  br label %264

; <label>:264:                                    ; preds = %262, %259
  br label %377

; <label>:265:                                    ; preds = %240
  %266 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %267 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.21, i32 0, i32 0), i64 %266)
  br label %377

; <label>:268:                                    ; preds = %240
  %269 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %270 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.21, i32 0, i32 0), i64 %269)
  br label %377

; <label>:271:                                    ; preds = %240
  %272 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  %273 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.22, i32 0, i32 0), double %272)
  %274 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.str.23, i32 0, i32 0)) #8
  %275 = icmp eq i32 %274, 0
  br i1 %275, label %276, label %281

; <label>:276:                                    ; preds = %271
  %277 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  store double %277, double* %40, align 8
  %278 = load double, double* %40, align 8
  %279 = fmul double %278, 1.000000e+12
  %280 = fptosi double %279 to i64
  store i64 %280, i64* @DTRes_pspr, align 8
  br label %281

; <label>:281:                                    ; preds = %276, %271
  %282 = call i32 @strcmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.24, i32 0, i32 0)) #8
  %283 = icmp eq i32 %282, 0
  br i1 %283, label %284, label %289

; <label>:284:                                    ; preds = %281
  %285 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  store double %285, double* %41, align 8
  %286 = load double, double* %41, align 8
  %287 = fmul double %286, 1.000000e+12
  %288 = fptosi double %287 to i64
  store i64 %288, i64* @TTRes_pspr, align 8
  br label %289

; <label>:289:                                    ; preds = %284, %281
  br label %377

; <label>:290:                                    ; preds = %240
  %291 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %292 = udiv i64 %291, 8
  %293 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str.25, i32 0, i32 0), i64 %292)
  %294 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %294, i64* @TTF_header_offset, align 8
  br label %377

; <label>:295:                                    ; preds = %240
  %296 = load double, double* bitcast (i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3) to double*), align 8
  %297 = call i64 @_Z15TDateTime_TimeTd(double %296)
  store i64 %297, i64* %42, align 8
  %298 = call %struct.tm* @gmtime(i64* %42) #7
  %299 = call i8* @asctime(%struct.tm* %298) #7
  %300 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %299, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.26, i32 0, i32 0))
  br label %377

; <label>:301:                                    ; preds = %240
  %302 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %303 = call noalias i8* @calloc(i64 %302, i64 1) #7
  store i8* %303, i8** %36, align 8
  %304 = load i8*, i8** %36, align 8
  %305 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %306 = load i8*, i8** %34, align 8
  store i8* %304, i8** %21, align 8
  store i64 1, i64* %22, align 8
  store i64 %305, i64* %23, align 8
  store i8* %306, i8** %24, align 8
  %307 = load i8*, i8** %21, align 8
  %308 = load i8*, i8** %24, align 8
  %309 = load i64, i64* @TTF_header_offset, align 8
  %310 = getelementptr inbounds i8, i8* %308, i64 %309
  %311 = load i64, i64* %22, align 8
  %312 = load i64, i64* %23, align 8
  %313 = mul i64 %311, %312
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %307, i8* align 1 %310, i64 %313, i1 false) #7
  %314 = load i64, i64* %22, align 8
  %315 = load i64, i64* %23, align 8
  %316 = mul i64 %314, %315
  %317 = load i64, i64* @TTF_header_offset, align 8
  %318 = add i64 %317, %316
  store i64 %318, i64* @TTF_header_offset, align 8
  %319 = load i64, i64* %22, align 8
  %320 = load i64, i64* %23, align 8
  %321 = mul i64 %319, %320
  %322 = trunc i64 %321 to i32
  store i32 %322, i32* %35, align 4
  %323 = load i32, i32* %35, align 4
  %324 = sext i32 %323 to i64
  %325 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %326 = icmp ne i64 %324, %325
  br i1 %326, label %327, label %330

; <label>:327:                                    ; preds = %301
  %328 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.27, i32 0, i32 0))
  %329 = load i8*, i8** %36, align 8
  call void @free(i8* %329) #7
  br label %425

; <label>:330:                                    ; preds = %301
  %331 = load i8*, i8** %36, align 8
  %332 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.15, i32 0, i32 0), i8* %331)
  %333 = load i8*, i8** %36, align 8
  call void @free(i8* %333) #7
  br label %377

; <label>:334:                                    ; preds = %240
  %335 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %336 = call noalias i8* @calloc(i64 %335, i64 1) #7
  %337 = bitcast i8* %336 to i32*
  store i32* %337, i32** %37, align 8
  %338 = load i32*, i32** %37, align 8
  %339 = bitcast i32* %338 to i8*
  %340 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %341 = load i8*, i8** %34, align 8
  store i8* %339, i8** %25, align 8
  store i64 1, i64* %26, align 8
  store i64 %340, i64* %27, align 8
  store i8* %341, i8** %28, align 8
  %342 = load i8*, i8** %25, align 8
  %343 = load i8*, i8** %28, align 8
  %344 = load i64, i64* @TTF_header_offset, align 8
  %345 = getelementptr inbounds i8, i8* %343, i64 %344
  %346 = load i64, i64* %26, align 8
  %347 = load i64, i64* %27, align 8
  %348 = mul i64 %346, %347
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %342, i8* align 1 %345, i64 %348, i1 false) #7
  %349 = load i64, i64* %26, align 8
  %350 = load i64, i64* %27, align 8
  %351 = mul i64 %349, %350
  %352 = load i64, i64* @TTF_header_offset, align 8
  %353 = add i64 %352, %351
  store i64 %353, i64* @TTF_header_offset, align 8
  %354 = load i64, i64* %26, align 8
  %355 = load i64, i64* %27, align 8
  %356 = mul i64 %354, %355
  %357 = trunc i64 %356 to i32
  store i32 %357, i32* %35, align 4
  %358 = load i32, i32* %35, align 4
  %359 = sext i32 %358 to i64
  %360 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %361 = icmp ne i64 %359, %360
  br i1 %361, label %362, label %366

; <label>:362:                                    ; preds = %334
  %363 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.27, i32 0, i32 0))
  %364 = load i32*, i32** %37, align 8
  %365 = bitcast i32* %364 to i8*
  call void @free(i8* %365) #7
  br label %425

; <label>:366:                                    ; preds = %334
  %367 = load i32*, i32** %37, align 8
  %368 = call i32 (i32*, ...) @wprintf(i32* getelementptr inbounds ([3 x i32], [3 x i32]* @.str.28, i32 0, i32 0), i32* %367)
  %369 = load i32*, i32** %37, align 8
  %370 = bitcast i32* %369 to i8*
  call void @free(i8* %370) #7
  br label %377

; <label>:371:                                    ; preds = %240
  %372 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  %373 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([32 x i8], [32 x i8]* @.str.29, i32 0, i32 0), i64 %372)
  %374 = load i64, i64* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 3), align 8
  store i64 %374, i64* @TTF_header_offset, align 8
  br label %377

; <label>:375:                                    ; preds = %240
  %376 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str.30, i32 0, i32 0))
  br label %425

; <label>:377:                                    ; preds = %371, %366, %330, %295, %290, %289, %268, %265, %264, %246, %244
  %378 = call i32 @strncmp(i8* getelementptr inbounds (%struct.TgHd, %struct.TgHd* @TagHead, i32 0, i32 0, i32 0), i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.31, i32 0, i32 0), i64 11) #8
  %379 = icmp ne i32 %378, 0
  br i1 %379, label %208, label %380

; <label>:380:                                    ; preds = %377
  %381 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.32, i32 0, i32 0))
  %382 = sext i32 %381 to i64
  store i64 %382, i64* @order_gurantee, align 8
  %383 = load i64, i64* @RecordType, align 8
  switch i64 %383, label %414 [
    i64 66051, label %384
    i64 66052, label %387
    i64 16843268, label %390
    i64 66053, label %393
    i64 66054, label %396
    i64 66307, label %399
    i64 66308, label %402
    i64 16843524, label %405
    i64 66309, label %408
    i64 66310, label %411
  ]

; <label>:384:                                    ; preds = %380
  %385 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.33, i32 0, i32 0))
  %386 = sext i32 %385 to i64
  store i64 %386, i64* @order_gurantee, align 8
  store i8 1, i8* %43, align 1
  br label %418

; <label>:387:                                    ; preds = %380
  %388 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.34, i32 0, i32 0))
  %389 = sext i32 %388 to i64
  store i64 %389, i64* @order_gurantee, align 8
  store i8 1, i8* %43, align 1
  br label %418

; <label>:390:                                    ; preds = %380
  %391 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.35, i32 0, i32 0))
  %392 = sext i32 %391 to i64
  store i64 %392, i64* @order_gurantee, align 8
  store i8 1, i8* %43, align 1
  br label %418

; <label>:393:                                    ; preds = %380
  %394 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.36, i32 0, i32 0))
  %395 = sext i32 %394 to i64
  store i64 %395, i64* @order_gurantee, align 8
  store i8 1, i8* %43, align 1
  br label %418

; <label>:396:                                    ; preds = %380
  %397 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.37, i32 0, i32 0))
  %398 = sext i32 %397 to i64
  store i64 %398, i64* @order_gurantee, align 8
  store i8 1, i8* %43, align 1
  br label %418

; <label>:399:                                    ; preds = %380
  %400 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.str.38, i32 0, i32 0))
  %401 = sext i32 %400 to i64
  store i64 %401, i64* @order_gurantee, align 8
  store i8 0, i8* %43, align 1
  br label %418

; <label>:402:                                    ; preds = %380
  %403 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.39, i32 0, i32 0))
  %404 = sext i32 %403 to i64
  store i64 %404, i64* @order_gurantee, align 8
  store i8 0, i8* %43, align 1
  br label %418

; <label>:405:                                    ; preds = %380
  %406 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.40, i32 0, i32 0))
  %407 = sext i32 %406 to i64
  store i64 %407, i64* @order_gurantee, align 8
  store i8 0, i8* %43, align 1
  br label %418

; <label>:408:                                    ; preds = %380
  %409 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.41, i32 0, i32 0))
  %410 = sext i32 %409 to i64
  store i64 %410, i64* @order_gurantee, align 8
  store i8 0, i8* %43, align 1
  br label %418

; <label>:411:                                    ; preds = %380
  %412 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str.42, i32 0, i32 0))
  %413 = sext i32 %412 to i64
  store i64 %413, i64* @order_gurantee, align 8
  store i8 0, i8* %43, align 1
  br label %418

; <label>:414:                                    ; preds = %380
  %415 = load i64, i64* @RecordType, align 8
  %416 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str.43, i32 0, i32 0), i64 %415)
  %417 = sext i32 %416 to i64
  store i64 %417, i64* @order_gurantee, align 8
  br label %425

; <label>:418:                                    ; preds = %411, %408, %405, %402, %399, %396, %393, %390, %387, %384
  %419 = load i8, i8* %43, align 1
  %420 = trunc i8 %419 to i1
  br i1 %420, label %421, label %422

; <label>:421:                                    ; preds = %418
  store i64 12495, i64* @SYNCRate_pspr, align 8
  br label %424

; <label>:422:                                    ; preds = %418
  %423 = load i64, i64* @TTRes_pspr, align 8
  store i64 %423, i64* @SYNCRate_pspr, align 8
  br label %424

; <label>:424:                                    ; preds = %422, %421
  store i64 4, i64* @BytesofRecords, align 8
  store i32 0, i32* %33, align 4
  br label %426

; <label>:425:                                    ; preds = %414, %375, %362, %327, %229, %201
  store i32 -1, i32* %33, align 4
  br label %426

; <label>:426:                                    ; preds = %424, %425
  %427 = load i32, i32* %33, align 4
  store i32 %427, i32* %51, align 4
  store i8 0, i8* %53, align 1
  br label %431

; <label>:428:                                    ; preds = %89
  %429 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([95 x i8], [95 x i8]* @.str.52, i32 0, i32 0))
  %430 = sext i32 %429 to i64
  store i64 %430, i64* @order_gurantee, align 8
  store i32 -2, i32* %51, align 4
  store i64 1, i64* @BytesofRecords, align 8
  br label %431

; <label>:431:                                    ; preds = %89, %428, %426, %164, %162, %124, %122
  %432 = load i64, i64* @NumRecords, align 8
  %433 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.str.53, i32 0, i32 0), i64 %432)
  %434 = sext i32 %433 to i64
  store i64 %434, i64* @order_gurantee, align 8
  %435 = load i32, i32* %51, align 4
  store i32 %435, i32* %48, align 4
  br label %436

; <label>:436:                                    ; preds = %431, %72
  %437 = load i32, i32* %48, align 4
  ret i32 %437
}

attributes #0 = { alwaysinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind }
attributes #2 = { alwaysinline uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #6 = { nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #7 = { nounwind }
attributes #8 = { nounwind readonly }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-3build1 (tags/RELEASE_801/final)"}
